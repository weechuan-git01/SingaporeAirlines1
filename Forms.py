from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, PasswordField, validators, FileField, \
    IntegerField
from wtforms.widgets import PasswordInput
from wtforms.fields.html5 import DateField, EmailField
from wtforms.validators import email_validator, Email, ValidationError
from datetime import date
from flask_wtf import RecaptchaField


def only_alp(form, field):
    for char in field.data:
        if char.isdigit():
            raise ValidationError('Please only input letters')


def only_numbers(form, field):
    for char in field.data:
        if char.isdigit() == False:
            raise ValidationError('Please only input numbers')


def validate_mobile_phone(form, field):
    if " " in field.data:
        raise ValidationError('Make sure there is no space between.')
    elif field.data.isdigit() == False:
        raise ValidationError('Phone number should only have numbers.')
    elif len(field.data) < 8:
        raise ValidationError('Phone number is not 8 digits')
    elif len(field.data) > 8:
        raise ValidationError('Phone number is not 8 digits')


class CreateEmployeeForm(Form):
    # login_id = StringField('Login id',[validators.DataRequired(), validators.Length(min=1, max=150)])
    # password = StringField('Password', [validators.DataRequired()], widget=PasswordInput(hide_value=False))
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired(), only_alp])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired(), only_alp])
    birthdate = DateField('Birthdate')
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    nationality = StringField('Nationality', [validators.Length(min=1, max=150), validators.DataRequired(), only_alp])
    photo = StringField('Photo', [validators.Length(min=1, max=150), validators.DataRequired()])
    role = SelectField('Role', [validators.DataRequired()],
                       choices=[('', 'Select'), ('C', 'Crew'), ('A', 'Admin'), ('M', 'Maintenance'), ('F', 'Flights'),
                                ('D', 'Declaration')], default='')
    employment_status = RadioField('Employment Status', [validators.DataRequired()],
                                   choices=[('E', 'Employed'), ('R', 'Retrenched')], default='')
    job_start_date = DateField('Job Start Date')

    level_of_education = StringField('Level of Education',
                                     [validators.DataRequired(), validators.Length(min=1, max=150)])
    major = StringField('Major', [validators.DataRequired(), validators.Length(min=1, max=150)])
    school = StringField('School', [validators.Length(min=1, max=150), validators.DataRequired()])
    graduation_date = DateField('Graduation Date')  # [validators.DataRequired()], format="%d/%m/%Y"

    address = StringField('Address', [validators.Length(min=1, max=150), validators.DataRequired()])
    mobile_contact = StringField('Mobile Number',
                                 [validators.Length(min=1, max=150), validators.DataRequired(), validate_mobile_phone])
    home_contact = StringField('Home Number',
                               [validators.Length(min=1, max=150), validators.DataRequired(), validate_mobile_phone])
    email = StringField('Email', [validators.Length(min=1, max=150), validators.DataRequired(), Email()])

    remarks = TextAreaField('Remarks', [validators.Optional()])


class CreateEmployerForm(Form):
    # login_id = StringField('Login id',[validators.DataRequired(), validators.Length(min=1, max=150)])
    # password = StringField('Password', [validators.DataRequired()], widget=PasswordInput(hide_value=False))
    company_name = StringField('Company Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    company_location = StringField('Company Location', [validators.Length(min=1, max=150), validators.DataRequired()])
    industry = StringField('Industry', [validators.Length(min=1, max=150), validators.DataRequired()])
    establishment_date = DateField('Establishment Date')
    company_logo = StringField('Company Logo')
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=1, max=150), Email()])
    contact = StringField('Contact Number',
                          [validators.DataRequired(), validators.Length(min=1, max=150), validate_mobile_phone])
    facebook = StringField('Facebook Link', [validators.DataRequired(), validators.Length(min=1, max=150)])
    instagram = StringField('Instagram Link', [validators.DataRequired(), validators.Length(min=1, max=150)])
    social_media = TextAreaField('Other Social Media Links', [validators.DataRequired()])
    website = StringField('Website', [validators.DataRequired(), validators.Length(min=1, max=150)])
    remarks = TextAreaField('Remarks', [validators.Optional()])


class CreateListingForm(Form):
    job_title = StringField('Job Title', [validators.DataRequired(), validators.Length(min=1, max=150)])
    no_of_hires = StringField('No, Of Hires',
                              [validators.DataRequired(), validators.Length(min=1, max=150), only_numbers])
    job_description = TextAreaField('Job Description', [validators.DataRequired()])
    job_requirements = TextAreaField('Job Requirements', [validators.DataRequired()])
    position_required = SelectField('Position Required', [validators.DataRequired()],
                                    choices=[('', 'Select'), ('A', 'Admin'), ('P', 'Pilot'), ('C', 'Crew'),
                                             ('M', 'Maintenance'), ('F', 'Flights')], default='')


class CreateAirplanesForm(Form):
    tail_number = StringField('Tail Number', [validators.Length(min=1, max=150), validators.DataRequired()])
    operation_status = RadioField('Operation Status', choices=[('Green', 'In Operation'), ('Red', 'Out of Operation')])
    model = SelectField('Model', [validators.DataRequired()],
                        choices=[('', 'Select'), ('Airbus A350-900', ' SIA Airbus A350-900'),
                                 ('Airbus A380-800', 'SIA Airbus A380-800'),
                                 ('Boeing 777-300ER', 'SIA Boeing 777-300ER'), ('Boeing 787-10', 'SIA Boeing 787-10'),
                                 ('Boeing B737-800NG', 'SLK B737-800NG'), ('Airbus A320-200', 'SLK A320-200'),
                                 ('Airbus A319-100', 'SLK A319-100'), ('Boeing B787-9', 'TGW B787-9'),
                                 ('Airbus A319', 'TGW A319')], default='')
    airline = SelectField('Airline', [validators.DataRequired()],
                          choices=[('', 'Select'), ('SIA', 'Singapore Airline'), ('SLK', 'Silk Airline'),
                                   ('TGW', 'Scoot')], default='')
    hanger = RadioField('Hanger', choices=[('SG', 'Changi Airport'), ('AUS', 'Alice Spring')])
    remarks = TextAreaField('Remarks', [validators.Optional()], default='-Nil-')
    last_maintenance = DateField('Last Maintenance')  # , format='%,/%d/%Y')
    in_charge = StringField('Maintenance In-Charge')


class CreateMaintenanceForm(Form):
    last_maintenance = DateField('Last Maintenance', [validators.Optional()])  # , format='%,/%d/%Y')
    in_charge = StringField('Maintenance In-Charge', [validators.Length(min=1), validators.DataRequired(), only_alp])


class CreatePassengerForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired(), only_alp])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired(), only_alp])
    nric = StringField('NRIC', [validators.Length(min=1, max=9), validators.DataRequired()])
    phone_no = StringField('Phone Number',
                           [validators.Length(min=1, max=8), validators.DataRequired(), validate_mobile_phone])
    email = StringField('Email', [validators.Length(min=1, max=150), validators.DataRequired(), Email()])
    flight_no = StringField('Flight No.', [validators.Length(min=1, max=5), validators.DataRequired()])
    seat_no = StringField('Seat No.', [validators.Length(min=1, max=5), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    health_declaration = RadioField('Health Declaration', choices=[('N', 'No'), ('Y', 'Yes'), ], default='N')
    pcr_test = RadioField('PCR Test', choices=[('N', 'No'), ('Y', 'Yes'), ], default='N')
    pre_book = RadioField('Pre-booked PCR Test', choices=[('N', 'No'), ('Y', 'Yes'), ], default='N')
    remarks = TextAreaField('Remarks', [validators.Optional()])


class CreateFlightForm(Form):
    flight_number = StringField('Flight Number', [validators.Length(min=1, max=150), validators.DataRequired()])
    departure_country = StringField('From', [validators.Length(min=1, max=150), validators.DataRequired()])
    arrival_country = StringField('To', [validators.Length(min=1, max=150), validators.DataRequired()])
    departure_date = DateField('Departure Date', format='%Y-%m-%d')
    fly = SelectField('Fly', [validators.DataRequired()], choices=[('', 'Select'), ('Y', 'Yes'), ('N', 'No')],
                      default='')
    flight_type = SelectField('Transit Or Direct', [validators.DataRequired()],
                              choices=[('', 'Select'), ('N', 'Direct'), ('Y', 'Transit')], default='')


class BookTicketForm(Form):
    departure_country = SelectField('From', [validators.DataRequired()],
                                    choices=[('', 'Select'), ('Singapore', 'Singapore')], default='')
    arrival_country = SelectField('To', [validators.DataRequired()],
                                  choices=[('', 'Select'), ('Hong Kong', 'Hong Kong'), ('Taipei', 'Taipei')], default='')
    return_date = DateField('Return Date', format='%Y-%m-%d', default=date.today())
    flight_class = SelectField('Class', [validators.DataRequired()],
                               choices=[('', 'Select'), ('Economy', 'Economy'), ('Premium Economy', 'Premium Economy'),
                                        ('Business', 'Business'), ('First/Suites', 'First/Suites')], default='')
    adults = SelectField('Adults', [validators.DataRequired()],
                         choices=[('', 'Select'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
                                  ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9')], default='')
    children = SelectField('Children', [validators.DataRequired()],
                           choices=[('', 'Select'), ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
                                    ('5', '5')], default='')


# class RegisterForm(Form):
#     type = SelectField('User Type', [validators.DataRequired()],
#                        choices=[('', 'Select'), ('Er', 'Employer')], default='')
#     login_id = StringField('Login id', [validators.DataRequired(), validators.Length(min=1, max=150)])
#     password = StringField('Password',
#                            [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords Must Match')],
#                            widget=PasswordInput(hide_value=False))
#     confirm = StringField('Confirm Password', [validators.DataRequired()], widget=PasswordInput(hide_value=False))


class RegisterForm(Form):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=1, max=150)])
    email = StringField('E-mail', [validators.DataRequired(), validators.Length(min=1, max=150)])
    password = StringField('Password',
                           [validators.DataRequired(), validators.EqualTo('confirm')],
                           widget=PasswordInput(hide_value=False))
    confirm = StringField('Repeat Password')
    recaptcha = RecaptchaField()


class LoginForm(Form):
    login_id = StringField('Login id', [validators.DataRequired(), validators.Length(min=1, max=150)])
    password = StringField('Password', [validators.DataRequired()], widget=PasswordInput(hide_value=False))
    recaptcha = RecaptchaField()


class ForgetPassword(Form):
    login_id = StringField('Login id', [validators.DataRequired(), validators.Length(min=1, max=150)])
    recaptcha = RecaptchaField()


class FilterStatus(Form):
    filter = SelectField('Filter Employment Status',
                         choices=[('All', 'All'), ('E', 'Employed'), ('R', 'Retrenched'), ('Resigned', 'Resigned')],
                         default='')


class FilterRole(Form):
    filter = SelectField('Filter Positions', [validators.DataRequired()],
                         choices=[('All', 'All'), ('C', 'Crew'), ('A', 'Admin'), ('M', 'Maintenance'), ('F', 'Flights'),
                                  ('D', 'Declaration')], default='')


class ChangePassword(Form):
    current_password = StringField('Current Password', [validators.DataRequired()],
                                   widget=PasswordInput(hide_value=False))
    new_password = StringField('New Password', [validators.DataRequired(),
                                                validators.EqualTo('confirm', message='Passwords Must Match')],
                               widget=PasswordInput(hide_value=False))
    confirm = StringField('Confirm Password', [validators.DataRequired()], widget=PasswordInput(hide_value=False))
