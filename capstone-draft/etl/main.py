from extract import get_appointment, get_councillor, get_patient_councillor, get_rating
from transform import extract_transform


def main():
    extract_transform(
        get_rating(), get_appointment(), get_patient_councillor(), get_councillor()
    )


if __name__ == "__main__":
    main()








