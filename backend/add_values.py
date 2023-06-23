from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Institution, User, Conference
from random import choice
from dotenv import load_dotenv
import os


def create_institutions(session):
    """Insert dummy institutions"""
    institutions_data = [
        {
            'institutionName': 'Institution 1',
            'institutionAddress': 'Address 1',
            'emailID': 'institution1@example.com',
            'contactNum': 1234567890,
            'membership': 'Choice1'
        },
        {
            'institutionName': 'Institution 2',
            'institutionAddress': 'Address 2',
            'emailID': 'institution2@example.com',
            'contactNum': 9876543210,
            'membership': 'Choice2'
        },
        {
            'institutionName': 'Institution 3',
            'institutionAddress': 'Address 3',
            'emailID': 'institution3@example.com',
            'contactNum': 4567890123,
            'membership': 'Choice1'
        },
        {
            'institutionName': 'Institution 4',
            'institutionAddress': 'Address 4',
            'emailID': 'institution4@example.com',
            'contactNum': 7890123456,
            'membership': 'Choice2'
        },
        {
            'institutionName': 'Institution 5',
            'institutionAddress': 'Address 5',
            'emailID': 'institution5@example.com',
            'contactNum': 3210987654,
            'membership': 'Choice1'
        }
    ]

    for data in institutions_data:
        institution = Institution(**data)
        session.add(institution)

    session.commit()


def set_roles(session: Session):
    """Create users of different roles and assign institutions randomly"""
    roles = {
        'SuperAdmin': 1,
        'Admin': 2,
        'Coordinator': 3,
        'Editor': 4,
        'AssociateEditor': 5,
        'Reviewer': 6,
        'Author': 7
    }

    # Create institutions
    create_institutions(session)

    def create_users(session: Session, role: str, count: int):
        """Create dummy users of a specific role"""
        users_data = [
            {
                'name': f'{role.capitalize()} {i}',
                'email': f'{role.lower()}{i}@example.com',
                'password': f'password{i}',
                'roleID': role
            }
            for i in range(1, count + 1)
        ]

        for user_data in users_data:
            user = User(**user_data)
            session.add(user)

        session.commit()

    for role, role_id in roles.items():
        count = 5 if role == 'SuperAdmin' else 10
        create_users(session, role, count)

        if role_id >= 2:
            users = session.query(User).filter(User.roleID == role_id).all()
            institutions: list[Institution] = session.query(Institution).all()

            for user in users:
                user.institutionID = choice(institutions).institutionID

    session.commit()


def create_conferences(session: Session):
    """Insert dummy conferences"""
    conferences_data = [
        {
            'conferenceTheme': 'Conference 1 Theme',
            'conferenceTrack': 'Conference 1 Track',
            'chairDesignation': 'Chair 1',
            'chairName': 'Chair Name 1',
        },
        {
            'conferenceTheme': 'Conference 2 Theme',
            'conferenceTrack': 'Conference 2 Track',
            'chairDesignation': 'Chair 2',
            'chairName': 'Chair Name 2',
        },
        {
            'conferenceTheme': 'Conference 3 Theme',
            'conferenceTrack': 'Conference 3 Track',
            'chairDesignation': 'Chair 3',
            'chairName': 'Chair Name 3',
        },
        {
            'conferenceTheme': 'Conference 4 Theme',
            'conferenceTrack': 'Conference 4 Track',
            'chairDesignation': 'Chair 4',
            'chairName': 'Chair Name 4',
        },
        {
            'conferenceTheme': 'Conference 5 Theme',
            'conferenceTrack': 'Conference 5 Track',
            'chairDesignation': 'Chair 5',
            'chairName': 'Chair Name 5',
        },
        {
            'conferenceTheme': 'Conference 6 Theme',
            'conferenceTrack': 'Conference 6 Track',
            'chairDesignation': 'Chair 6',
            'chairName': 'Chair Name 6',
        }
    ]

    for data in conferences_data:
        coordinator = choice(session.query(
            User).filter(User.roleID == 3).all())
        if coordinator is None:
            continue
        data['inCharge'] = coordinator.userID
        conference = Conference(**data)
        session.add(conference)

    session.commit()


def main():
    load_dotenv(".env")
    engine = create_engine(os.environ.get('DB_URL'))

    with Session(engine) as session:
        set_roles(session)
        create_conferences(session)


# Run the main function
if __name__ == '__main__':
    main()
