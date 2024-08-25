import uuid

from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response

from account.service.account_service_impl import AccountServiceImpl
from google_oauth.service.google_oauth_service_impl import GoogleOauthServiceImpl
from google.oauth2 import id_token
from google.auth.transport import requests

from google_oauth.service.redis_service_impl import RedisServiceImpl


class GoogleOauthView(viewsets.ViewSet):
    googleOauthService = GoogleOauthServiceImpl.getInstance()
    redisService = RedisServiceImpl.getInstance()
    accountService = AccountServiceImpl.getInstance()

    def GoogleLoginToken(self, request):
        token = request.data.get('credential')
        clientId = request.data.get('clientId')
        try:
            tokenInfo = id_token.verify_oauth2_token(token, requests.Request(), clientId)

            userInfo = self.googleOauthService.googleTokenDecoding(tokenInfo)

            return Response({
                'sub': userInfo['sub'],
                'name': userInfo['name'],
                'email': userInfo['email'],
            }, status=200)
        except Exception as e:
            print("토큰 인코딩 오류 발생:", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def redisAccessToken(self, request):
        try:
            email = request.data.get('email')
            print(f"redisAccessToken -> email: {email}")
            account = self.accountService.findAccountByEmail(email)
            print(account)
            if not account:
                return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

            userToken = str(uuid.uuid4())
            print(f"type of account.id: {type(account.id)}")
            ticket = self.accountService.findTicketByAccountId(account.id)
            nickname = self.accountService.findNicknameByAccountId(account.id)
            cherry = self.accountService.findCherryByAccountId(account.id)
            attendance_cherry = self.accountService.findAttendance_CherryByAccountId(account.id)
            attendance_date = self.accountService.findAttendance_DateByAccountId(account.id)

            self.redisService.store_access_token(userToken, str(account.id), nickname, email, ticket, cherry,
                                                 attendance_cherry, attendance_date)

            return Response({'userToken': userToken}, status=status.HTTP_200_OK)
        except Exception as e:
            print('redisAccessToken()', e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def getUserTokenEmailInfo(self, request):
        try:
            userToken = request.data.get('usertoken')
            print(f"Searching for token: {userToken}")
            stored_data = self.redisService.getValueByKey(userToken)
            print(f"Stored data: {stored_data}")

            if not stored_data:
                return Response({'error': 'Token not found'}, status=status.HTTP_404_NOT_FOUND)

            email = stored_data.get('email', '')
            account_id = stored_data.get('account_id', '')

            print(f"Account ID: {account_id}, Email: {email}")

            return Response({'EmailInfo': email}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f'Error retrieving email info: {e}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def getUserTokenPaidMemberTypeInfo(self, request):
        try:
            userToken = request.data.get('usertoken')
            accountId = self.redisService.getValueByKey(userToken)
            print(f"accountId: {accountId}")
            PaidMemberTypeInfo = self.accountService.findPaidMemberTypeByAccountId(accountId)

            return Response({'PaidMemberTypeInfo': PaidMemberTypeInfo}, status=status.HTTP_200_OK)
        except Exception as e:
            print('Error storing access token in Redis:', e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def getUserTicketInfo(self, request):
        try:
            userToken = request.data.get('usertoken')
            accountInfo = self.redisService.getValueByKey(userToken)
            print(f"accountId 입니다: {accountInfo}")
            ticket = accountInfo['ticket']
            print("티켓만 출력", ticket)
            return Response({'ticket': ticket}, status=status.HTTP_200_OK)
        except Exception as e:
            print('Error retrieving ticket info:', e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def getUserNicknameInfo(self, request):
        try:
            userToken = request.data.get('usertoken')
            accountInfo = self.redisService.getValueByKey(userToken)
            print(f"accountId 입니다: {accountInfo}")
            nickname = accountInfo['nickname']
            print("닉네임 출력", nickname)
            return Response({'nickname': nickname}, status=status.HTTP_200_OK)
        except Exception as e:
            print('Error retrieving nickname info:', e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def updateUserTicket(self, request):
        try:
            user_token = request.data.get('usertoken')
            print("updateUserTicket() 유저토큰", user_token)
            accountInfo = self.redisService.getValueByKey(user_token)
            account_id = accountInfo['account_id']
            print("updateUserTicket() 어카운트ID", account_id)

            ticket = self.accountService.findTicketByAccountId(account_id)
            if ticket <= 0:
                return False, "No tickets available"

            new_ticket_count = ticket - 1
            self.accountService.updateTicketCount(account_id, new_ticket_count)

            accountInfo['ticket'] = new_ticket_count
            self.redisService.update_access_token(user_token, accountInfo)
            return Response({'ticket': ticket}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error using ticket: {e}")
            return False, str(e)

    def getUserCherryInfo(self, request):
        try:
            userToken = request.data.get('usertoken')
            accountInfo = self.redisService.getValueByKey(userToken)
            print(f"accountId 입니다: {accountInfo}")
            cherry = accountInfo['cherry']
            print("티켓만 출력", cherry)
            return Response({'cherry': cherry}, status=status.HTTP_200_OK)
        except Exception as e:
            print('Error retrieving cherry info:', e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def getUserAttendanceCherryInfo(self, request):
        try:
            userToken = request.data.get('usertoken')
            accountInfo = self.redisService.getValueByKey(userToken)
            print(f"accountId 입니다: {accountInfo}")
            cherry = accountInfo['cherry']
            print("티켓만 출력", cherry)
            return Response({'cherry': cherry}, status=status.HTTP_200_OK)
        except Exception as e:
            print('Error retrieving cherry info:', e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def purchaseTicket(self, request):
        try:
            user_token = request.data.get('usertoken')
            accountInfo = self.redisService.getValueByKey(user_token)
            purchaseTicket = request.data.get('ticket')
            account_id = accountInfo['account_id']

            ticket = self.accountService.findTicketByAccountId(account_id)
            if ticket <= 0:
                return False, "티켓 없음"

            new_ticket_count = ticket + purchaseTicket
            self.accountService.updateTicketCount(account_id, new_ticket_count)

            accountInfo['ticket'] = new_ticket_count
            self.redisService.update_access_token(user_token, accountInfo)
            return Response({'ticket': ticket}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error purchase ticket: {e}")
            return False, str(e)

    def updateUserCherry(self, request):
        try:
            user_token = request.data.get('usertoken')
            accountInfo = self.redisService.getValueByKey(user_token)
            account_id = accountInfo['account_id']
            updateCherry = request.data.get('cherry')
            cherry = self.accountService.findCherryByAccountId(account_id)
            if cherry <= 0:
                return False, "No tickets available"

            new_cherry_count = cherry - updateCherry
            self.accountService.updateCherryCount(account_id, new_cherry_count)

            accountInfo['cherry'] = new_cherry_count
            self.redisService.update_cherry_count(user_token, accountInfo)
            return Response({'cherry': cherry}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error using ticket: {e}")
            return False, str(e)

    def purchaseCherry(self, request):
        try:
            user_token = request.data.get('usertoken')
            accountInfo = self.redisService.getValueByKey(user_token)
            purchaseCherry = request.data.get('cherry')
            account_id = accountInfo['account_id']

            cherry = self.accountService.findCherryByAccountId(account_id)

            new_cherry_count = cherry + purchaseCherry
            self.accountService.updateCherryCount(account_id, new_cherry_count)

            accountInfo['cherry'] = new_cherry_count
            self.redisService.update_cherry_count(user_token, accountInfo)
            return Response({'cherry': cherry}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error purchase cherry: {e}")
            return False, str(e)
