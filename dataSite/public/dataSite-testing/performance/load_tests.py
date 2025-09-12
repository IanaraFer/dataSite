from locust import HttpUser, task, between

class DataSightUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def load_test_data_upload(self):
        with open('test_data/valid_samples/sample_business_data.csv', 'rb') as file:
            self.client.post("/upload", files={"file": file})

    @task
    def load_test_forecasting(self):
        self.client.get("/forecast?days=30")

    @task
    def load_test_analysis(self):
        self.client.get("/analyze")