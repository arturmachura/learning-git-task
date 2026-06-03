from faker import Faker

fake = Faker("pl_PL")


class BaseContact:
    def __init__(self, first_name, last_name, phone, email):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email

    @property
    def label_length(self):
        return len(f"{self.first_name} {self.last_name}")

    def contact(self):
        print(f"Wybieram numer {self.phone} i dzwonię do {self.first_name} {self.last_name}")


class BusinessContact(BaseContact):
    def __init__(self, first_name, last_name, phone, email, position, company, work_phone):
        super().__init__(first_name, last_name, phone, email)
        self.position = position
        self.company = company
        self.work_phone = work_phone

    def contact(self):
        print(f"Wybieram numer {self.work_phone} i dzwonię do {self.first_name} {self.last_name}")


def create_contacts(contact_type, count):
    contacts = []
    for _ in range(count):
        if contact_type == BaseContact:
            contacts.append(BaseContact(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=fake.phone_number(),
                email=fake.email(),
            ))
        elif contact_type == BusinessContact:
            contacts.append(BusinessContact(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=fake.phone_number(),
                email=fake.email(),
                position=fake.job(),
                company=fake.company(),
                work_phone=fake.phone_number(),
            ))
    return contacts


if __name__ == "__main__":
    base = create_contacts(BaseContact, 2)
    business = create_contacts(BusinessContact, 2)

    print("=== Wizytówki prywatne ===")
    for c in base:
        print(f"{c.first_name} {c.last_name} | email: {c.email} | długość etykiety: {c.label_length}")
        c.contact()

    print("\n=== Wizytówki firmowe ===")
    for c in business:
        print(f"{c.first_name} {c.last_name} | {c.position} @ {c.company} | długość etykiety: {c.label_length}")
        c.contact()
