# this file is to check and validate user stories


#for test
#=======
from datetime import datetime

error_locations = []

def story_validation(individuals, families):
    # To print Errors
    print(("ERRORS".center(80, ' ')))
    print("\nUser Story             Description:                             "
          "     Location")
    print(('-' * 80))

    # Sprint 1
    birth_before_marriage(individuals, families)


###########################################################################################

#US02 - Birth should occur before marriage of that individual
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

# report Error to the console
def report_error(error_type, description, locations):
    #report("ERROR", error_type, description, locations)

    if isinstance(locations, list):
        locations = ','.join(locations)

    estr = '{:14.14s}  {:50.50s}    {:10.10s}' \
        .format(error_type, description, locations)
    print(estr)

    error_locations.extend(locations)


