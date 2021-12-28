class Status:

    INACTIVATE = "I"
    ACTIVATE = "A"
    LOCKED = "L"

    INACTIVATE_NAME = "Inactivate"
    ACTIVATE_NAME = "Activate"
    LOCKED_NAME = "Locked"

    CHOICES = ((INACTIVATE, INACTIVATE_NAME), (ACTIVATE, ACTIVATE_NAME), (LOCKED, LOCKED_NAME))
    NAME_LIST = [INACTIVATE_NAME, ACTIVATE_NAME, LOCKED_NAME]
    CODE_LIST = [INACTIVATE, ACTIVATE, LOCKED]
    SELECT_LIST = [dict(text=INACTIVATE_NAME, value=INACTIVATE), dict(text=ACTIVATE_NAME, value=ACTIVATE),
                   dict(text=LOCKED_NAME, value=LOCKED)]


class Gender:

    NONE = ""
    MALE = "M"
    FEMALE = "F"

    NONE_NAME = ""
    MALE_NAME = "Male"
    FEMALE_NAME = "Female"

    CHOICES = ((NONE, NONE_NAME), (MALE, MALE_NAME), (FEMALE, FEMALE_NAME))
    NAME_LIST = [NONE_NAME, MALE_NAME, FEMALE_NAME]
    CODE_LIST = [NONE, MALE, FEMALE]
    SELECT_LIST = [dict(text=NONE_NAME, value=NONE), dict(text=MALE_NAME, value=MALE),
                   dict(text=FEMALE_NAME, value=FEMALE)]


class UserRole:

    ADMIN = "A"
    LOGISTICS = "L"
    USER = "U"

    ADMIN_NAME = "Admin"
    LOGISTICS_NAME = "Logistics"
    USER_NAME = "User"

    CHOICES = ((ADMIN, ADMIN_NAME), (LOGISTICS, LOGISTICS_NAME), (USER, USER_NAME))
    NAME_LIST = [ADMIN_NAME, LOGISTICS_NAME, USER_NAME]
    CODE_LIST = [ADMIN, LOGISTICS, USER]
    SELECT_LIST = [dict(text=ADMIN_NAME, value=ADMIN), dict(text=LOGISTICS_NAME, value=LOGISTICS),
                   dict(text=USER_NAME, value=USER)]
    DICT = {ADMIN: ADMIN_NAME, LOGISTICS: LOGISTICS_NAME, USER: USER_NAME}

    @classmethod
    def get_name(cls, role_code):
        return cls.DICT.get(role_code, '')


class AccountICStatus:

    PENDING = "P"
    APPROVED = "A"
    REJECTED = "R"

    PENDING_NAME = "Pending"
    APPROVED_NAME = "Approved"
    REJECTED_NAME = "Rejected"

    CHOICES = ((PENDING, PENDING_NAME), (APPROVED, APPROVED_NAME), (REJECTED, REJECTED_NAME))
    NAME_LIST = [PENDING_NAME, APPROVED_NAME, REJECTED_NAME]
    CODE_LIST = [PENDING, APPROVED, REJECTED]
    SELECT_LIST = [dict(text=PENDING_NAME, value=PENDING), dict(text=APPROVED_NAME, value=APPROVED),
                   dict(text=REJECTED_NAME, value=REJECTED)]


class AccountICImageType:

    NRIC_FRONT = "NRIC"
    SELFIE = "SELFIE"

    NRIC_FRONT_NAME = "Front NRIC"
    SELFIE_NAME = "Selfie"

    CHOICES = ((NRIC_FRONT, NRIC_FRONT_NAME), (SELFIE, SELFIE_NAME))
    NAME_LIST = [NRIC_FRONT_NAME, SELFIE_NAME]
    CODE_LIST = [NRIC_FRONT, SELFIE]


class PointActionType:

    TAKE_SAMPLE_NAME = "Take Sample"
    WRITE_REVIEW = "Write Review"
    PURCHASE_SAMPLING_ITEM = "Purchase Sampling Item"
