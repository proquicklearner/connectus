from chat.utils import find_or_create_private_chat
from django.db import models
from django.conf import settings
from django.db.models.expressions import F
from django.utils import timezone



class FriendList(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    friends     = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,related_name="friends")


    
    def __str__(self):
        return self.user.username

    def add_friend(self, user):

        if not user in self.friends.all():
            self.friends.add(user)
            self.save()

            chat = find_or_create_private_chat(self.user, user)
            if not chat.is_active:
                chat.is_active = True
                chat.save()




    def remove_friend(self, user):

        if user in self.friends.all():
            self.friends.remove(user)

            chat = find_or_create_private_chat(self.user, user)
            if chat.is_active:
                chat.is_active = False
                chat.save()


    def unfriend(self,removee):

        remover_friend_list = self

        remover_friend_list.remove_friend(removee)


        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)


    def is_mutual_friend(self,friend):

        if friend in self.friends.all():
            return True
        return False

    
class FriendRequest(models.Model):

    sender          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="sender")
    receiver        = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="receiver")

    is_active       = models.BooleanField(blank=True,null=False,default=True)
    timestamp        = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.sender.username

    def accept(self):

        receiver_friend_list = FriendList.objects.get(user=self.receiver)

        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        self.is_active = False
        self.save()


    def cancel(self):
        self.is_active = False
        self.save()


