from locust import HttpLocust, TaskSet

def sumbission(l):
    response = l.client.post("/", {"gcs_uri":"gs://vijays-test-bucket/final-result.mp4",
                        "api_key":"AIzaSyCPZJ3_hlLTcdMtkBEzXHXIuGkmNn1TeFc", "sample_rate":"1"})
    print(response.text)

class UserBehavior(TaskSet):
    tasks = {sumbission:1}

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5000
    max_wait=5000