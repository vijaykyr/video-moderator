import argparse
import base64
import cv2
import os
import re

from apiclient.discovery import build
from oauth2client.client import GoogleCredentials
from timer import Timer

# Author: reddyv@
# Last Update: 03-13-2016
# Usage:
#   python vid_moderator.py --help
# Todo:
#   1) Evaluate using ffmpeg instead of OpenCV. Can you get faster than 
#   200ms/frame? This is the current performance bottleneck
#   2) Figure out why application default credentials don't work for vision API
#   3) See if you can convert the cv2 image format to base64 directly in memory 
#   without having to write to disk first. Note this is lower priority because
#   the disk read/write time is still an order of magnitude less than the frame
#   grabbing time (10ms vs 200ms), at least on SSD storage

def moderate(file_name, sample_rate, APIKey):
  BATCH_LIMIT = 8 #number of images to send per API request. Documented limit
  # is 16 images per request but i've tested up to 150 per request with success
  
  #obtain service handle for vision API using API Key
  #Note: would prefer to use application default credentials rather than API key
  # but get the following error when i try. Appears to be trying to authenticate
  # to a different project than the one specified during gcloud init
  """googleapiclient.errors.HttpError: <HttpError 403 when requesting
   https://vision.googleapis.com/v1/images:annotate?alt=json returned "Project 
   has not activated the vision.googleapis.com API. Please enable the API for 
   project google.com:cloudsdktool (#32555940559).">"""
   
  service = build('vision', 'v1', 
  discoveryServiceUrl='https://vision.googleapis.com/$discovery/rest?version=v1',
  developerKey=APIKey)
  
  #initialize vars 
  position = 0
  frame = 0
  batch_count = 0
  base64_images = [] 
  
  if file_name.lower().startswith('gs://'): #download file from gcs
    #get application default credentials (specified during gcloud init)
    credentials = GoogleCredentials.get_application_default()

    #construct service handle
    gcs_service = build('storage', 'v1', credentials=credentials)

    #extract GCS bucket and object from file name
    re_match = re.match(r'gs://(.*?)/(.*)', file_name, re.I)
    
    #'get_media' returns file contents while 'get' returns file metadata
    req = gcs_service.objects().get_media(bucket=re_match.group(1), 
      object=re_match.group(2))

    #execute request and save response to disk
    with open('temp.mp4','w') as file:
      file.write(req.execute())
      file_name = 'temp.mp4'
    
  #grab first frame
  #format note: this has been tested with the mp4 video format ONLY     
  vidcap = cv2.VideoCapture(file_name)
  success,image = vidcap.read()
  html_response = ''
  
  while success: 
    
    with Timer('Batch Total'):
      
      #read in frames one batch at a time
      while success and batch_count < BATCH_LIMIT:
      
        #convert frame to base64
        cv2.imwrite('temp.jpg', image) 
        with open('temp.jpg','rb') as image:
          base64_images.append((position/1000,base64.b64encode(image.read())))
      
        
        #advance to next image
        if sample_rate > 0: position = position+1000*sample_rate
        else: position = -1 #terminate
        frame += 1
        batch_count += 1
        vidcap.set(0,position)
        
        #vicap.read() takes ~200ms per frame on macbook air 
        #this is the performance bottleneck
        with Timer('Read frame'): success,image = vidcap.read()
  
      #send batch to vision API
      json_request = {'requests': []}
      for img in base64_images:
        json_request['requests'].append(
          {
            'image': {
              'content': img[1] #recall img is a tuple (timestamp, base64image)
             },
            'features': [
             {
              'type': 'SAFE_SEARCH_DETECTION',
             },
             {
              'type': 'LABEL_DETECTION',
              'maxResults': 3,
             },
             {
              'type': 'LOGO_DETECTION',
              'maxResults': 3,
             },
             {
              'type': 'TEXT_DETECTION',
              'maxResults': 3,
             }
             ] 
          })
      
      service_request = service.images().annotate(body=json_request)
      
      #API performance
      # tl;dr: the more you batch the better
      #  1 frame batch takes ~1 sec
      #  10 frame batch takes ~1.5 sec
      #  100 frame batch takes ~4.0 sec
      # Note these numbers should drop a bit when running the app from the cloud
      # due to reduced latency. But relative differences should hold.
      with Timer('API request'): responses = service_request.execute()

      #response format
      #{u'responses': [{u'labelAnnotations': [{u'score': 0.99651724, u'mid':
      # u'/m/01c4rd', u'description': u'beak'}, {u'score': 0.96588981, u'mid':
      # u'/m/015p6', u'description': u'bird'}, {u'score': 0.85704041, u'mid':
      # u'/m/09686', u'description': u'vertebrate'}]}]}

      #process response and print results
      if responses.has_key('responses'):
        for response, img in zip(responses.get('responses'),base64_images):
         
          #print frame timestamp
          html_response += ('<h3>'+str(img[0])+'sec</h3>')
          
          #process labels
          html_response += ('\tLabels:')
          if response.has_key('labelAnnotations'):
            html_response += printEntityAnnotation(response.get('labelAnnotations'))
          else: html_response += ('no labels identified<br>')
          
          #process logos
          html_response += ('\tLogos:')
          if response.has_key('logoAnnotations'):
            html_response += printEntityAnnotation(response.get('logoAnnotations'))
          else: html_response += ('no logos identified<br>')
          
          #process safe search
          html_response += ('\tSafe Search:<br>')
          if response.has_key('safeSearchAnnotation'):
            html_response += ('\t  Adult Content is '+
              response.get('safeSearchAnnotation').get('adult') + '<br>')
            html_response += ('\t  Violent Content is '+
              response.get('safeSearchAnnotation').get('violence') + '<br>')
          else: html_response += ('\t\tno safe search results<br>')
          
          #process text (OCR-optical character recognition)
          html_response += ('\tText:')
          if response.has_key('textAnnotations'):
            html_response += printEntityAnnotation(response.get('textAnnotations'))
          else: html_response += ('no text identified<br>')
          
      else: html_response += ('no response<br>')
      
      #reset for next batch
      batch_count = 0
      base64_images = []

  
  #cleanup
  os.remove('temp.jpg')
  if os.path.isfile('temp.mp4'): os.remove('temp.mp4')

  return html_response

def printEntityAnnotation(annotations):
  entities = ''
  for annotation in annotations:
    entities += annotation['description']+', '
  entities = entities[:-2] #trim trailing comma and space
  
  #added this try/except because Vision API was returning non-unicode text for OCR
  try:
    entities + '<br>'
  except UnicodeEncodeError as err:
    return err
  return entities + '<br>'
if __name__ == '__main__':
  
  #configure command line options
  parser = argparse.ArgumentParser(
    description='Feed a video to the Google Vision API')
  parser.add_argument(
    'file_name', help=('The video you\'d like to process. Can either pass a '
    'local file or a GCS file in the format "gs://<bucket-name>/<file'
    '-path>"'))
  parser.add_argument(
    'APIKey', help=('The API Key that identifies your Google Cloud Console '
    'Project with Vision API Enabled'))
  parser.add_argument(
    '-s','--sample-rate',dest='samplerate', default=5, type=int, 
    help=('The rate at which stills should be sampled from the '
    'video. Default is 5 (one frame per 5 seconds).'))
  
  #read in command line arguments
  args = parser.parse_args()
  
  #start execution
  with Timer('Total'): moderate(args.file_name, args.samplerate, args.APIKey)
