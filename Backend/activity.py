class ActivityManager(object):
    def getActivity(self, userId):
        #TODO: get all activity from DB of userId
        return []

    def addActivity(self, activity):
        #TODO: add activity to DB
        return True
    
    def checkActivity(self, userId, activityId):
        #TODO: check if activity has correct parameters
        return True
    
    def updateActivity(self, userId, activityId, status):
        #TODO: update activity
        return True

    def exists(self, activity):
        #TODO: check if activity already exists
        return False

class Activity:
    def __init__(self, access, date):
        self.access = access
        self.date = date

    def __repr__(self):
        #TODO: complete when you have the definitive form for the access object
        return f'<Access: {self.access}>'