import requests
import os
from .common import message_templates

api_key = os.environ.get("SMS_CHEF_API_KEY")
device_id = os.environ.get("SMS_CHEF_DEVICE_ID")
country_code = "+63"


class BulkSMS:
    def __init__(self):
        self.students = {}
        self.message_template = ""

    def send(self, message_template=None):
        if not message_template:
            message_template = self.message_template

        for student_id, student_info in self.students.items():
            self._send_single(
                student_info["contact_number"],
                self._generate_message(message_template, student_info),
            )

    def _generate_message(self, message_template, student):
        pass

    def _send_single(self, recipient_no, message):
        recipient_no = self._preprocess_numbers([recipient_no])[0]
        single_message_url = "https://www.cloud.smschef.com/api/send/sms"
        message_params = {
            "secret": api_key,
            "mode": "devices",
            "device": device_id,
            "sim": 1,
            "priority": 1,
            "phone": recipient_no,
            "message": message,
        }
        request = requests.post(url=single_message_url, params=message_params)
        result = request.json()

        return result

    def _preprocess_numbers(self, numbers):
        preprocessed = []

        for number in numbers:
            if number[:3] != country_code:
                shift = 1 if number[0] == "0" else 0
                number = country_code + number[shift:]
                preprocessed.append(number)

        return preprocessed


class IncompleteGradeSMS(BulkSMS):
    def __init__(self, grades):
        super().__init__()
        self.message_template = message_templates["incomplete_grade"]
        self._process_grades(grades)

    def _process_grades(self, grades):
        for grade in grades:
            student_id = grade["student_id"]

            if student_id not in self.students:
                self.students[student_id] = {
                    "first_name": grade["student_info"]["first_name"],
                    "middle_name": grade["student_info"]["middle_name"],
                    "last_name": grade["student_info"]["last_name"],
                    "contact_number": grade["student_info"]["contact_number"],
                    "subjects": [],
                }

            self.students[student_id]["subjects"].append(
                f"{grade['subjects']['title']} (Year: {grade['year']}, Sem: {grade['sem']})"
            )

    def _generate_message(self, message_template, student):
        return message_template.format(
            first_name=student["first_name"],
            middle_name=student["middle_name"],
            last_name=student["last_name"],
            subjects=", ".join(student["subjects"]),
        )


class FailedGradeSMS(IncompleteGradeSMS):
    def __init__(self, grades):
        super().__init__(grades)
        self.message_template = message_templates["failed_grade"]


class DocumentsSMS(BulkSMS):
    def __init__(self, documents):
        super().__init__()

        self.message_template = message_templates["requested_document"]

        self._process_documents(documents)

    def _process_documents(self, documents):
        for document in documents:
            student_id = document["student_id"]

            if student_id not in self.students:
                self.students[student_id] = {
                    "first_name": document["student_info"]["first_name"],
                    "middle_name": document["student_info"]["middle_name"],
                    "last_name": document["student_info"]["last_name"],
                    "contact_number": document["student_info"]["contact_number"],
                    "document": document["document_type"]["type"],
                }

    def _generate_message(self, message_template, student):
        return message_template.format(
            first_name=student["first_name"],
            middle_name=student["middle_name"],
            last_name=student["last_name"],
            document=student["document"],
        )
