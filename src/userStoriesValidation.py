# this file is to check and validate user stories

from datetime import datetime
from dateutil.relativedelta import relativedelta

error_locations = []

def story_validation(individuals, families):
    # To print Errors
    print(("ERRORS/ANOMALIES".center(120, ' ')))
    print("\nError/Anomalies:        User Story             Description:                             "
          "     Location")
    print(('-' * 120))

    # Sprint 1
    dates_before_current(individuals, families)
    birth_before_marriage(individuals, families)
    birth_before_death(individuals)
    us05(individuals, families)
    us07(individuals)
    us06(individuals,families)
    marriage_before_divorce(families)
    us08(individuals, families)
    #Sprint 2
    us11(individuals, families)

####################################################################
# US01 All dates must be before the current date - ERROR
def dates_before_current(individuals, families):
    return_flag = True
    error_type = "US01"

    for indiv in individuals:
        if indiv.birthday and indiv.birthday > datetime.now().date():
            error_descrip = "Birth occurs after current date"
            error_location = [indiv.uid]
            report_error('ERROR', error_type, error_descrip, error_location)
            return_flag = False

        if indiv.deathDate and indiv.deathDate > datetime.now().date():
            error_descrip = "Death occurs after current date"
            error_location = [indiv.uid]
            report_error('ERROR', error_type, error_descrip, error_location)
            return_flag = False

    for family in families:
        if family.marriage and family.marriage > datetime.now().date():
            error_descrip = "Marriage occurs after current date"
            error_location = [family.uid, family.husband, family.wife]
            report_error('ERROR',error_type, error_descrip, error_location)
            return_flag = False

        if family.divorce and family.divorce > datetime.now().date():
            error_descrip = "Divorce occurs after current date"
            error_location = [family.uid, family.husband, family.wife]
            report_error('ERROR',error_type, error_descrip, error_location)
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
                report_error('ERROR',error_type, error_descrip, error_location)
                return_flag = False

            if husband.birthday and husband.birthday > family.marriage:
                error_descrip = "Birth of husband occurs after marraige"
                error_location = [husband.uid]
                report_error('ERROR',error_type, error_descrip, error_location)
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
                report_error('ERROR',error_type, error_descrip, error_location)
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
                    report_error('ERROR',error_type, error_descrip, error_location)
                    return_flag = False

            if husband.alive == False:
                if  family.marriage > husband.deathDate:
                    error_descrip = "Death of Husband occurs before marriage"
                    error_location = [husband.uid]
                    report_error('ERROR',error_type, error_descrip, error_location)
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
            report_error('ERROR',error_type,error_descrip,error_location)
            return_flag= False
        if indiv.alive == True and relativedelta(today,indiv.birthday).years > 150:
            error_descrip = "lived longer than 150 years"
            error_location = indiv.uid
            report_error('ERROR',error_type, error_descrip, error_location)
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
                report_error('ERROR',error_type, error_descrip, error_location)
                return_flag = False
    return return_flag

# US06 Divorce before Death
def us06(individuals, families):
    # For each individual check if divorce occurs before death
    return_flag = True
    error_type = "US06"
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
                    error_descrip = "Death of Wife occurs before divorce"
                    error_location = [wife.uid]
                    report_error('ERROR',error_type, error_descrip, error_location)
                    return_flag = False

            if husband.alive == False:
                if  family.divorce > husband.deathDate:
                    error_descrip = "Death of Husband occurs before divorce"
                    error_location = [husband.uid]
                    report_error('ERROR',error_type, error_descrip, error_location)
                    return_flag = False

    return return_flag

################################################################################################
def us08(individuals, families):
    return_flag = True
    error_type = "US08"
    for family in families:
        if family.marriage:
            # Search through individuals to get husband and wife
            child = []
            for indiv in individuals:
                id = indiv.uid
                bday = indiv.birthday
                if id in family.children and family.divorce is not None:
                    if bday < family.marriage:
                        error_descrip = "Birth occurs before marriage"
                        error_location = [indiv.uid]
                        report_error('ERROR',error_type, error_descrip, error_location)
                        return_flag = False
                    if relativedelta(bday,family.divorce).months+9:
                        error_descrip="Birth after divorce of 9 months"
                        error_location=[indiv.uid]
                        report_error('ERROR',error_type,error_descrip,error_location)
                        return_flag=False
    return return_flag
#####################################################################################
#US11
def us11(individuals,families):
    return_flag = True
    error_type = "US11"
    bigamy=[]
    check = []
    for family in families:
        if family.marriage:
            husband = None
            wife = None
            first_current_marriage = True
            first_marriage_start = family.marriage
            for indiv in individuals:
                if indiv.uid == family.husband:
                    husband = indiv
                if indiv.uid == family.wife:
                    wife = indiv
            if family.divorce!=None:
                first_current_marriage = False
                first_marriage_end=family.divorce


            else:
                if wife.alive == False and husband.alive == False:
                    if wife.deathDate < husband.deathDate:
                        first_marriage_end = wife.deathDate
                        first_current_marriage = False
                    else:
                        first_marriage_end = husband.deathDate
                        first_current_marriage = False
                else:
                    if wife.alive==False:
                        first_marriage_end=wife.deathDate
                        first_current_marriage = False
                    if husband.alive==False:
                        first_marriage_end=husband.deathDate
                        first_current_marriage = False

            # Search through individuals to get husband and wife
            for family2 in families:
                #find the spouse
                if family.marriage != family2.marriage:
                    if family2.marriage:
                        husband2 = None
                        wife2 = None
                        second_current_marriage = True
                        second_marriage_start = family2.marriage
                        for indiv1 in individuals:
                            if indiv1.uid == family2.husband:
                                husband2 = indiv1
                            if indiv1.uid == family2.wife:
                                wife2 = indiv1
                        if family2.divorce != None:
                            second_current_marriage = False
                            second_marriage_end = family2.divorce
                        else:
                            if wife2.alive==False and husband2.alive==False:
                                if wife2.deathDate<husband2.deathDate:
                                    second_marriage_end = wife2.deathDate
                                    second_current_marriage = False
                                else:
                                    second_marriage_end = husband2.deathDate
                                    second_current_marriage = False
                            else:
                                if wife2.alive == False:
                                    second_marriage_end = wife2.deathDate
                                    second_current_marriage = False
                                if husband2.alive == False:
                                    second_marriage_end = husband2.deathDate
                                    second_current_marriage = False
                        if husband.uid==husband2.uid or wife.uid==wife2.uid:

                            if first_current_marriage== True and second_current_marriage==True:
                                if husband.uid==husband2.uid:
                                    check.append((husband.uid))
                                    for element in check:
                                        if element not in bigamy:
                                            bigamy.append((husband.uid))
                                            error_descrip = "Bigamy Occurs in family"
                                            error_location = [family.uid ,family2.uid,husband.uid]
                                            report_error(error_type, error_descrip, error_location)
                                            return_flag = False
                                if wife.uid==wife2.uid:
                                    check.append((wife.uid))
                                    for element in check:
                                        if element not in bigamy:
                                            bigamy.append((wife.uid))
                                            error_descrip = "Bigamy Occurs in family"
                                            error_location = [family.uid ,family2.uid, wife.uid]
                                            report_error(error_type, error_descrip, error_location)
                                            return_flag = False
                            else:
                                if first_marriage_start > second_marriage_start:
                                    s_m_s = first_marriage_start
                                    f_m_s = second_marriage_start
                                    second_marriage_start=s_m_s
                                    first_marriage_start=f_m_s
                                    f_m_e=second_marriage_end
                                    second_marriage_end=first_marriage_end
                                    first_marriage_end=f_m_e

                                if first_marriage_end != None  and second_marriage_end!=None:
                                    if first_marriage_end > second_marriage_start :
                                        if husband.uid == husband2.uid:
                                            check.append((husband.uid))
                                            for element in check:
                                                if element not in bigamy:
                                                    bigamy.append(( husband.uid))
                                                    error_descrip = "Bigamy Occurs in family"
                                                    error_location = [family.uid ,family2.uid ,husband.uid]
                                                    report_error(error_type, error_descrip, error_location)
                                                    return_flag = False
                                        if wife.uid == wife2.uid:
                                            check.append((wife.uid))
                                            for element in check:
                                                if element not in bigamy:
                                                    bigamy.append(( wife.uid))
                                                    error_descrip = "Bigamy Occurs in families and the bigamist is "
                                                    error_location = [family.uid ,family2.uid, wife.uid]
                                                    report_error(error_type, error_descrip, error_location)
                                                    return_flag = False

    return return_flag

# report Error to the console
def report_error(rtype, error_type, description, locations):
    # report("ERROR", error_type, description, locations)

    if isinstance(locations, list):
        locations = ','.join(locations)

    estr = '{:26.7s} {:14.14s}  {:50.50s}    {:50.50s}' \
        .format(rtype, error_type, description, locations)
    print(estr)


    error_locations.extend(locations)



