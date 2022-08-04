from DataManagement.DataObjects.sessionInfo import SessionInfo
from DataManagement.DataStacks.sessionInfoDataStack import SessionInfoDataStack



class SessionInfoDataStackInterface:
    @staticmethod
    def updateSessionInfo():
        sessionInfoData = SessionInfoDataStack.getData()
        sessionInfo = SessionInfo.fromData(sessionInfoData)
        sessionInfo.changePrevUpdate()
        newSessionInfoData = sessionInfo.toData()
        SessionInfoDataStack.setData(newSessionInfoData)