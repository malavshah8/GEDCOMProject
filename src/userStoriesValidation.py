# this file is to check and validate user stories

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from collections import Counter

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
    marriage_before_divorce(families)
    us05(individuals, families)
    us06(individuals, families)
    us07(individuals)
    us08(individuals, families)

    #Sprint 2
    birth_before_death_of_parents(individuals, families)
    us10(individuals, families)
    us11(individuals, families)
    us12(individuals, families)
    multiple_births_less_5(individuals, families)
    us15(families)
    us16(individuals, families)
    us17(families)

    #Sprint 3
    no_sibling_marriage(individuals, families)
    us21(individuals, families)
    us22(individuals, families)
    us23(individuals,families)
    us25(individuals, families)
    list_deceased(individuals)
    us30(individuals, families)
    us31(individuals,families)


    # Sprint 4
    us32(individuals, families)
    us33(individuals, families)
    us35(individuals)
    us36(individuals)
    living_spouses(individuals, families)
    sibling_spacing(individuals, families)
    us38(individuals)
    us39(families)

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

####################################################################
# US09 - Birth before death of parents
def birth_before_death_of_parents(individuals, families):
    return_flag = True
    error_type = "US09"

    for individual in individuals:

        if len(individual.famc) > 0:
            father = None
            father_id = None
            mother = None
            mother_id = None
            fam = None

            # Get the UID of parents for an individual
            for family in families:
                if family.uid == individual.famc[0]:
                    father_id = family.husband
                    mother_id = family.wife
                    fam = family
                    break

            # Get the UID of individuals
            for ind in individuals:
                if ind.uid == father_id:
                    father = ind
                if ind.uid == mother_id:
                    mother = ind

            if father.deathDate is not None and father.deathDate < individual.birthday - timedelta(days=266):
                error_descrip = "Child is born more than 9 months or after death of father"
                error_location = [fam.uid, individual.uid]
                report_error('ERROR',error_type, error_descrip, error_location)
                return_flag = False

            if mother.deathDate is not None and mother.deathDate < individual.birthday:
                error_descrip = "Child is born after death of mother"
                error_location = [fam.uid, individual.uid]
                report_error('ERROR',error_type, error_descrip, error_location)
                return_flag = False
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
                                            report_error('ERROR',error_type, error_descrip, error_location)
                                            return_flag = False
                                if wife.uid==wife2.uid:
                                    check.append((wife.uid))
                                    for element in check:
                                        if element not in bigamy:
                                            bigamy.append((wife.uid))
                                            error_descrip = "Bigamy Occurs in family"
                                            error_location = [family.uid ,family2.uid, wife.uid]
                                            report_error('ERROR',error_type, error_descrip, error_location)
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
                                                    report_error('ERROR',error_type, error_descrip, error_location)
                                                    return_flag = False

    return return_flag
##########################################################

#US14  -  No more than five siblings should be born at the same time

def multiple_births_less_5(individuals,families):

    error_type = "US14"
    return_flag = True

    for family in families:
        sibling_uids = family.children
        siblings = list(x for x in individuals if x.uid in sibling_uids)
        sib_birthdays = []
        for sibling in siblings:
            sib_birthdays.append(sibling.birthday)
        result = Counter(sib_birthdays).most_common(1)
        for (a,b) in result:
            if b > 5:
                error_descrip = "More than 5 siblings born at once"
                error_location = [family.uid]
                report_error('ERROR',error_type, error_descrip, error_location)
                return_flag = False

    return return_flag

#########################################################
# US16
def us16(individuals,families):
    return_flag = True
    error_type = "US16"
    for family in families:
        if family.marriage:
            # Search through individuals to get husband and wife
            lastname=family.husbandName[1]
            for indiv in individuals:
                id=indiv.uid
                name=indiv.name
                gender=indiv.sex
                if id in family.children:
                    if gender == "M":
                        if lastname not in name:
                            error_descrip = "Lastname not the same as father "
                            error_location = [indiv.uid]
                            report_error('ERROR',error_type, error_descrip, error_location)
                            return_flag = False

    return return_flag

#########################################################

def us15(families):
    """ US15 - Families should not have more than 15 children - ANOMALY """
    error_type = "US15"
    return_flag = True

    for family in families:
        if len(family.children) >= 15:
            error_descrip = "Family has 15 or more siblings"
            error_location = [family.uid]
            report_error('ERROR', error_type, error_descrip, error_location)
            return_flag = False
    return return_flag

##############################################################

def us10(individuals, families):
    """ US10 - Marriage should be atleast 14 years after the birth of both spouses"""

    error_type = "US10"
    return_flag = True

    curr_date = datetime.today()
    min_birt = datetime(curr_date.year - 14,
                        curr_date.month, curr_date.day)

    for family in families:
        husband = None
        wife = None
        for individual in individuals:
            if individual.uid == family.husband:
                husband = individual
            if individual.uid == family.wife:
                wife = individual

            if husband is not None and wife is not None:
                break

        if husband.birthday > min_birt.date():
            error_descrip = "Husband is married before 14 years old"
            error_location = [family.uid, husband.uid]
            report_error('ANOMALY',error_type, error_descrip, error_location)
            return_flag = False

        if wife.birthday > min_birt.date():
            error_descrip = "Wife is married before 14 years old"
            error_location = [family.uid, wife.uid]
            report_error('ANOMALY',error_type, error_descrip, error_location)
            return_flag = False
    return return_flag

#################################################################



def us12(individuals, families):
    return_flag = True
    error_type = "US12"



    for individual in individuals:

        if len(individual.famc) > 0:
            father = None
            father_id = None
            mother = None
            mother_id = None
            fam = None

            # Get the UID of parents for an individual
            for family in families:
                if family.uid == individual.famc[0]:
                    father_id = family.husband
                    mother_id = family.wife
                    fam = family
                    break

            # Get the UID of individuals
            for ind in individuals:
                if ind.uid == father_id:
                    father = ind
                if ind.uid == mother_id:
                    mother = ind

            if father.birthday is not None and father.birthday < individual.birthday - timedelta(days=29200):
                error_descrip = "Father is older than 80 years"
                error_location = [fam.uid, individual.uid]
                report_error('ERROR',error_type, error_descrip, error_location)
                return_flag = False

            if mother.birthday is not None and mother.birthday < individual.birthday - timedelta(days=21900):
                error_descrip = "Mother is older than 60 years"
                error_location = [fam.uid, individual.uid]
                report_error('ERROR',error_type, error_descrip, error_location)
                return_flag = False
    return return_flag

#############################################################################################################
 #Parents should not marry any of their descendants
def us17(families):
   
    error_type = "US17"
    return_flag = True

    for family in families:
        decendants = []

        decendants.extend(family.children)
        for decendant in decendants:
            temp_decs = return_children(decendant, families)
            if temp_decs is not None:
                decendants.extend(temp_decs)

        if family.husband and family.wife and family.wife in decendants:
            error_descrip = "Wife is decendant of spouse"
            error_location = [family.wife, family.husband]
            report_error('ERROR',error_type, error_descrip, error_location)
            return_flag = False

        if family.husband and family.wife and family.husband in decendants:
            error_descrip = "Husband is decendant of spouse"
            error_location = [family.wife, family.husband]
            report_error('ERROR',error_type, error_descrip, error_location)
            return_flag = False
    return return_flag

 ### Helper function for no_marriage_to_decendants
def return_children(uid, families):
    
    # find family where uid is a Parents
    family = next((x for x in families if x.husband == uid), None)
    if family is None:
        family = next((x for x in families if x.wife == uid), None)

    if family is None:  # Is never a parent
        return None
    else:
        return family.children

################################################################################################

def us21(individuals, families):
    """ US21 - Correct Gender for Role; husband should be male, wife should
    be female  """
    error_type = "US21"
    return_flag = True

    for family in families:
        husband_id = family.husband
        wife_id = family.wife

        husband = None
        wife = None

        for individual in individuals:
            if individual.uid == husband_id:
                husband = individual
            if individual.uid == wife_id:
                wife = individual

        if husband.sex is not "M":
            error_descrip = "Husband is not a male"
            error_location = [husband.uid, family.uid]
            report_error('ANOMALY',error_type, error_descrip, error_location)
            return_flag = False

        if wife.sex is not "F":
            error_descrip = "Wife is not a female"
            error_location = [wife.uid, family.uid]
            report_error('ANOMALY',error_type, error_descrip, error_location)
            return_flag = False
    return return_flag

###################################################################################

def us30(individuals, families):
    """ US30 - List all Married People in the families. """
    error_type = "US30"
    return_flag = True

    for family in families:
        husband_id = family.husband
        wife_id = family.wife

        husband = None
        wife = None

        for individual in individuals:
            if individual.uid == husband_id:
                husband = individual
            if individual.uid == wife_id:
                wife = individual

        if husband.alive is True and wife.alive is True:
            error_descrip = "Both Husband and Wife are not dead"
            error_location = [family.uid]
            report_error('-', error_type, error_descrip, error_location)
            return_flag = False

    return return_flag

################################################################################3
""" US23 - No more than one individual with the same name and birth date should appear in a GEDCOM file"""
def us23(individuals, families):
    
    error_type = "US23"
    return_flag = True

    for individual in individuals:
        for compare_indiv in individuals:
            if individual.name and compare_indiv.name \
                    and individual.name == compare_indiv.name:
                # same name, compare birthdate
                if compare_indiv.birthday and individual.birthday \
                        and compare_indiv.birthday and individual.birthday:

                    error_descrip = "Two individuals share a name and birthdate"
                    error_location = [individual.uid, compare_indiv.uid]
                    report_error('ERROR', error_type, error_descrip, error_location)
                    return_flag = False

    return return_flag

#######################################################################################################


def us21(individuals, families):
    """ US21 - Correct Gender for Role; husband should be male, wife should
    be female  """
    error_type = "US21"
    return_flag = True

    for family in families:
        husband_id = family.husband
        wife_id = family.wife

        husband = None
        wife = None

        for individual in individuals:
            if individual.uid == husband_id:
                husband = individual
            if individual.uid == wife_id:
                wife = individual

        if husband.sex is not "M":
            error_descrip = "Husband is not a male"
            error_location = [husband.uid, family.uid]
            report_error('ANOMALY',error_type, error_descrip, error_location)
            return_flag = False

        if wife.sex is not "F":
            error_descrip = "Wife is not a female"
            error_location = [wife.uid, family.uid]
            report_error('ANOMALY',error_type, error_descrip, error_location)
            return_flag = False
    return return_flag

###################################################################################

def us30(individuals, families):
    """ US30 - List all Married People in the families. """
    error_type = "US30"
    return_flag = True

    for family in families:
        husband_id = family.husband
        wife_id = family.wife

        husband = None
        wife = None

        for individual in individuals:
            if individual.uid == husband_id:
                husband = individual
            if individual.uid == wife_id:
                wife = individual

        if husband.alive is True and wife.alive is True:
            error_descrip = "Both Husband and Wife are not dead"
            error_location = [family.uid]
            report_error('INFORMATION', error_type, error_descrip, error_location)
            return_flag = False

    return return_flag



###################################################
# US22
def us22(individuals,families):
    """ US 22- Check for unique IDS"""
    error_type="US22"
    return_flag = True
    seen = set()
    notseen=set()
    uniq = []
    check=[]
    for indiv in individuals:
        indiv_id=indiv.uid
        check.append(indiv_id)
    for family in families:
        fam_id=family.uid
        check.append(fam_id)
    for x in check:
        if x not in seen:
            seen.add(x)
        else:
            notseen.add(x)
    for dup in notseen:
        error_descrip = "Duplicate ID Found"
        error_location = [dup]
        report_error('Error', error_type, error_descrip, error_location)
        return_flag = False
    return return_flag

###########################################################################################
#US31
def us31(individuals, families):
    """ US31 - List all Single People. """
    error_type = "US31"
    return_flag = True
    curr_date= datetime.now()
    check=[]
    for family in families:
        husb = family.husband
        wife = family.wife
        check.append(husb)
        check.append(wife)
    for individual in individuals:
        indiv =individual.uid
        bday = individual.birthday
        if relativedelta(curr_date,bday).years > 30:
            if indiv not in check:
                error_descrip = "Single and over thirty"
                error_location = [indiv]
                report_error('INFORMATION', error_type, error_descrip, error_location)
                return_flag = False

    return return_flag
########################################################################

# US35 Anyone born in the last 30 days
def us35(individuals):
    error_type = "US35"
    return_flag = True
    curr_date = datetime.today()


    for individual in individuals:
        indiv = individual.uid
        bday = individual.birthday
        diff=(curr_date.date()-bday).days
        if diff<= 30:
                error_descrip = "Born in the last 30 days:"
                error_location = [indiv]
                report_error('INFORMATION', error_type, error_descrip, error_location)
                return_flag = False

    return return_flag
########################################
# US36 Anyone died in the last 30 days
def us36(individuals):
    error_type = "US36"
    return_flag = True
    curr_date = datetime.today()

    for individual in individuals:
        indiv = individual.uid
        if individual.alive==False:
            deathday = individual.deathDate
            diff=(curr_date.date()-deathday).days
        if diff<= 30:
                error_descrip = "Died in the last 30 days:"
                error_location = [indiv]
                report_error('INFORMATION', error_type, error_descrip, error_location)
                return_flag = False

    return return_flag


########################################################################
"""No more than one child with the same name and birth date should appear in a family """
def us25(individuals,families):
    error_type = "US25"
    return_flag = True
    for family in families:
        if family.marriage is not None:
            if len(family.children) != 0:
                childFirstName= family.children[0]
            else:
                continue
            for indiv in individuals:
                id= indiv.uid
                name=indiv.name
                if id in family.children:
                    if childFirstName in name:
                        error_descrip="Child's Firstname is not unique"
                        error_location= [indiv.uid]
                        report_error('ERROR',error_type,error_descrip,error_location)
                        return_flag= False

    return return_flag

######################################################################

# US18 - Siblings should not marry one another - ANOMALY """

def no_sibling_marriage(individuals, families):
    error_type = "US18"
    return_flag = True

    for family in families:
        sibling_uids = family.children
        siblings = list(x for x in individuals if x.uid in sibling_uids)

        for sibling in siblings:
            sib_fam = next((x for x in families if x.husband == sibling.uid),None)

            if sib_fam and sib_fam.wife in sibling_uids:
                error_descrip = "Sibling is married to another sibling"
                error_location = [sibling.uid, sib_fam.wife]
                report_error("ERROR",error_type,error_descrip, error_location)
                return_flag = False

    return return_flag

######################################################################

#US29 - List the deceased individuals
def list_deceased(individuals):
    error_type = "US29"
    return_flag = True

    for individual in individuals:
        if individual.deathDate is not None:
            error_descrip = "Deceased individuals"
            error_location = [individual.uid]
            report_error('INFORMATION', error_type, error_descrip, error_location)
            return_flag = False

    return return_flag


######################################################################

#US37
def living_spouses(individuals,families):
    error_type = "US37"
    return_flag = True
    curr_date = datetime.now().date()

    for individual in individuals:
        indiv = individual.uid
        if individual.alive == False:
            deathday = individual.deathDate
            diff = (curr_date - deathday).days
        if diff <= 30 and len(individual.fams) > 0:
            for family in families:
                if family.uid == individual.fams[0]:
                    husband_id = family.husband
                    wife_id = family.wife
                    error_descrip = "Living Spouses"
                    error_location = [wife_id,husband_id]
                    report_error('INFORMATION', error_type, error_descrip, error_location)
                    return_flag = False

    return return_flag

######################################################################

#US13
def sibling_spacing(individuals,families):
    error_type = "US13"
    return_flag = True

    for family in families:
        sibling_uids = family.children
        siblings = list(x for x in individuals if x.uid in sibling_uids)

        sib_birthdays = sorted(siblings, key=lambda ind: ind.birthday, reverse=False)
        i=0
        count = len(sib_birthdays)
        while i < count-1:
            diff = sib_birthdays[i+1].birthday - sib_birthdays[i].birthday
            if (diff > timedelta(days=2) and diff < timedelta(days=243)):
                error_descrip = "Difference in sibling age impossible!"
                error_location = [sib_birthdays[i+1].uid, sib_birthdays[i].uid]
                report_error("ERROR",error_type, error_descrip, error_location)
                return_flag = False
            i+=1
        return return_flag

#######################################################################

#US42
def illegitimate_dates(individuals):
    error_type = "US42"
    return_flag = True

    for individual in individuals:
        indiv = individual.uid
        date = individual.birthday
        date_text = str(date)
        if not datetime.strptime(date_text, '%Y-%m-%d'):
            error_descrip = "Illegitimate Dates"
            error_location = [indiv]
            report_error('ERROR', error_type, error_descrip, error_location)
            return_flag = False

    return return_flag

# US 32 - Multiple Birth in GEDCOM file
######################################################################################################
def us32(individuals,families):

    error_type = "US32"
    return_flag = True

    for family in families:
        sibling_uids = family.children
        siblings = list(x for x in individuals if x.uid in sibling_uids)
        sib_birthdays = []
        for sibling in siblings:
            sib_birthdays.append(sibling.birthday)
        result = Counter(sib_birthdays).most_common(1)
        for (a,b) in result:
            if b > 2:
                error_descrip = "Multiple Birth in Family"
                error_location = [family.uid]
                report_error('ANAMOLY',error_type, error_descrip, error_location)
                return_flag = False

    return return_flag


###################################################################################
def us30(individuals, families):
    """ US30 - List all Married People in the families. """
    error_type = "US30"
    return_flag = True

    for family in families:
        husband_id = family.husband
        wife_id = family.wife

        husband = None
        wife = None

        for individual in individuals:
            if individual.uid == husband_id:
                husband = individual
            if individual.uid == wife_id:
                wife = individual

        if husband.alive is True and wife.alive is True:
            error_descrip = "Both Husband and Wife are not dead"
            error_location = [family.uid]
            report_error('INFORMATION', error_type, error_descrip, error_location)
            return_flag = False

    return return_flag


###################################################################################
def us33(individuals, families):
    """ US33 - List all orphan children. """
    error_type = "US33"
    return_flag = True

    for family in families:
        husband_id = family.husband
        wife_id = family.wife

        husband = None
        wife = None

        if len(family.children) == 0:
            break

        for individual in individuals:
            if individual.uid == husband_id:
                husband = individual
            if individual.uid == wife_id:
                wife = individual

        if husband.alive is False and wife.alive is False:
            siblings = list(x for x in individuals if x.uid in family.children)
            for child in siblings:
                if calculate_age(child.birthday) < 18:
                    error_descrip = "Orphan Children"
                    error_location = [family.uid, child.uid]
                    report_error('INFORMATION', error_type, error_descrip, error_location)
                    return_flag = False

    return return_flag


def calculate_age(born):
    today = datetime.today().date()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


######################################################################
def us38(individuals):
    error_type = "US38"
    return_flag = True
    curr_date = datetime.today()


    for individual in individuals:
        indiv = individual.uid
        if individual.alive == True:
            
            bday = individual.birthday
            bday = datetime(curr_date.year,bday.month,bday.day)
            upcoming_birthday=(bday - curr_date).days
            if upcoming_birthday<= 30 and upcoming_birthday >= 0:
                    error_descrip = "Birthday is coming in next 30 days"
                    #error_descrip = str(upcoming_birthday)
                    error_location = [indiv]
                    report_error('INFORMATION', error_type, error_descrip, error_location)
                    return_flag = False

    return return_flag

###########################################################################  
def us39(families):
    error_type = "US39"
    return_flag = True
    curr_date = datetime.today()


    for family in families:
        if family.marriage:
            family_id= family.uid
            M_date = family.marriage
            M_date = datetime(curr_date.year,M_date.month,M_date.day)
            upcoming_Anniversary = (M_date - curr_date).days
            if upcoming_Anniversary<= 30 and upcoming_Anniversary >= 0:
                 error_descrip = "Anniversary is coming in next 30 days"
                 error_location = [family_id]
                 report_error('INFORMATION', error_type, error_descrip, error_location)
                 return_flag = False
            
            

    return return_flag
##################################################################################      


# report Error to the console
def report_error(rtype, error_type, description, locations):
    # report("ERROR", error_type, description, locations)

    if isinstance(locations, list):
        locations = ','.join(locations)

    estr = '{:26.12s} {:14.14s}  {:50.50s}    {:50.50s}' \
        .format(rtype, error_type, description, locations)
    print(estr)


    error_locations.extend(locations)



