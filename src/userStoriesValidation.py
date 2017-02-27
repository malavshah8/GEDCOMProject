# this file is to check and validate user stories

from datetime import datetime
from datetime import date
from unittest import TestCase
from dateutil.relativedelta import relativedelta
error_locations = []


def story_validation(individuals, families):
    # To print Errors
    print(("ERRORS".center(80, ' ')))
    print("\nUser Story             Description:                             "
          "     Location")
    print(('-' * 80))

    # Sprint 1
    dates_before_current(individuals, families)
    birth_before_marriage(individuals, families)
    birth_before_death(individuals)
    us05(individuals, families)
    us07(individuals)


####################################################################
# US01 All dates must be before the current date - ERROR
def dates_before_current(individuals, families):
    return_flag = True
    error_type = "US01"

    for indiv in individuals:
        if indiv.birthday and indiv.birthday > datetime.now().date():
            error_descrip = "Birth occurs after current date"
            error_location = [indiv.uid]
            report_error(error_type, error_descrip, error_location)
            return_flag = False

        if indiv.deathDate and indiv.deathDate > datetime.now().date():
            error_descrip = "Death occurs after current date"
            error_location = [indiv.uid]
            report_error(error_type, error_descrip, error_location)
            return_flag = False

    for family in families:
        if family.marriage and family.marriage > datetime.now().date():
            error_descrip = "Marriage occurs after current date"
            error_location = [family.uid, family.husband, family.wife]
            report_error(error_type, error_descrip, error_location)
            return_flag = False

        if family.divorce and family.divorce > datetime.now().date():
            error_descrip = "Divorce occurs after current date"
            error_location = [family.uid, family.husband, family.wife]
            report_error(error_type, error_descrip, error_location)
            return_flag = False

    return return_flag

###########################################################################################

# US02 - Birth should occur before marriage of that individual
def birth_before_marriage(individuals, families):
    # For each individual check if birth occurs before marriage
    return_flag = True
    error_type = "US02"
    for family in families:
        if family.marriage:
            # Search through individuals to get husband and wife
            husband = None
            wife = None

            for indiv in individuals:
                if indiv.uid == family.husband:
                    husband = indiv
                if indiv.uid == family.wife:
                    wife = indiv

            if wife.birthday and wife.birthday > family.marriage:
                # Found a case spouse marries before birthday
                error_descrip = "Birth of wife occurs after marriage"
                error_location = [wife.uid]
                report_error(error_type, error_descrip, error_location)
                return_flag = False

            if husband.birthday and husband.birthday > family.marriage:
                error_descrip = "Birth of husband occurs after marraige"
                error_location = [husband.uid]
                report_error(error_type, error_descrip, error_location)
                return_flag = False

    return return_flag

#US03 - Birth should occur before death of an individual

def birth_before_death(individuals):

    return_flag = True
    error_type = "US03"
    for individual in individuals:
        if individual.deathDate and individual.birthday:
            if individual.deathDate < individual.birthday:
                error_descrip = "Birth occurs before death."
                error_location = [individual.uid]
                report_error(error_type, error_descrip, error_location)
                return_flag = False
    return return_flag

########################################################################
#US05 Marriage before Death
def us05(individuals, families):

    # For each individual check if marriage occurs before death
    return_flag = True
    error_type = "US05"
    for family in families:
        if family.marriage:
            # Search through individuals to get husband and wife
            husband = None
            wife = None

            for indiv in individuals:
                if indiv.uid == family.husband:
                    husband = indiv
                if indiv.uid == family.wife:
                    wife = indiv

            if wife.alive == False:
                if family.marriage < wife.deathDate:
                    # Found a case spouse marries before birthday
                    error_descrip = "Death of Wife occurs before marriage"
                    error_location = [wife.uid]
                    report_error(error_type, error_descrip, error_location)
                    return_flag = False

            if husband.alive == False:
                if  family.marriage > husband.deathDate:
                    error_descrip = "Death of Husband occurs before marriage"
                    error_location = [husband.uid]
                    report_error(error_type, error_descrip, error_location)
                    return_flag = False

    return return_flag
#################################################
# US07 Checks whether a person lived for more than 150 years.
def us07(individuals):
    return_flag = True
    error_type = "US07"
    today=datetime.now()
    for indiv in individuals:
        person=indiv.uid
        if indiv.alive == False and relativedelta(indiv.deathDate, indiv.birthday).years > 150:
            error_descrip="lived longer than 150 years"
            error_location = indiv.uid
            report_error(error_type,error_descrip,error_location)
            return_flag= False
        if indiv.alive == True and relativedelta(today,indiv.birthday).years > 150:
            error_descrip = "lived longer than 150 years"
            error_location = indiv.uid
            report_error(error_type, error_descrip, error_location)
            return_flag = False
    return return_flag

#################################################
# US04 Checks Marriage before Divorce.
def marriage_before_divorce(families):
    return_flag = True
    error_type = "US04"
    for family in families:
        if family.marriage and family.divorce:
            if family.marriage > family.divorce:
                error_descrip = "Marriage occurs after divorce"
                error_location = [family.uid, family.husband, family.wife]
                report_error(error_type, error_descrip, error_location)
                return_flag = False
    return return_flag

# report Error to the console
def report_error(error_type, description, locations):
    # report("ERROR", error_type, description, locations)

    if isinstance(locations, list):
        locations = ','.join(locations)

    estr = '{:14.14s}  {:50.50s}    {:10.100s}' \
        .format(error_type, description, locations)
    print(estr)


    error_locations.extend(locations)
    
    ##################################################
    #US07 Divorce before Death
def us07(individuals, families):

    # For each individual check if divorce occurs before death
    return_flag = True
    error_type = "US07"
    for family in families:
        if family.divorce:
            # Search through individuals to get husband and wife
            husband = None
            wife = None

            for indiv in individuals:
                if indiv.uid == family.husband:
                    husband = indiv
                if indiv.uid == family.wife:
                    wife = indiv

            if wife.alive == False:
                if family.divorce < wife.deathDate:
                    # Found a case spouse marries before birthday
                    error_descrip = "Death of Wife occurs before marriage"
                    error_location = [wife.uid]
                    report_error(error_type, error_descrip, error_location)
                    return_flag = False

            if husband.alive == False:
                if  family.divorce > husband.deathDate:
                    error_descrip = "Death of Husband occurs before marriage"
                    error_location = [husband.uid]
                    report_error(error_type, error_descrip, error_location)
                    return_flag = False

    return return_flag

# report Error to the console
def report_error(error_type, description, locations):
    # report("ERROR", error_type, description, locations)

    if isinstance(locations, list):
        locations = ','.join(locations)

    estr = '{:14.14s}  {:50.50s}    {:10.10s}' \
        .format(error_type, description, locations)
    print(estr)


    error_locations.extend(locations)



