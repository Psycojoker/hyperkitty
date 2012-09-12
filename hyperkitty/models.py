# -*- coding: utf-8 -*-
# Copyright (C) 1998-2012 by the Free Software Foundation, Inc.
#
# This file is part of HyperKitty.
#
# HyperKitty is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# HyperKitty is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# HyperKitty.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Aamir Khan <syst3m.w0rm@gmail.com>
# 

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from kittystore import get_store

from hyperkitty.utils import log


class Rating(models.Model):
    # @TODO: instead of list_address, user list model from kittystore?
    list_address = models.CharField(max_length=50)

    # @TODO: instead of messsageid, use message model from kittystore?
    messageid = models.CharField(max_length=100)

    user = models.ForeignKey(User)

    vote = models.SmallIntegerField()

    def __unicode__(self):
        """Unicode representation"""
        if self.vote == 1:
              return u'id = %s : %s voted up %s' % (self.id, unicode(self.user), self.messageid)
        else:
            return u'id = %s : %s voted down %s' % (self.id, unicode(self.user), self.messageid)


class UserProfile(models.Model):
    # User Object
    user = models.OneToOneField(User)

    karma = models.IntegerField(default=1)

    def _get_votes(self):
        "Returns all the votes by a user"
        # Extract all the votes by this user
        try:
            votes = Rating.objects.filter(user=self.user)
        except Rating.DoesNotExist:
            votes = {}

        # TODO: warning, not thread-safe, should get the cached connection from
        # the WSGI environment
        store = get_store(settings.KITTYSTORE_URL)
        for vote in votes:
            list_name = vote.list_address.split('@')[0]
            message = store.get_message_by_id_from_list(vote.list_address, vote.messageid)
            vote.message = message

        return votes

    votes = property(_get_votes)

    def __unicode__(self):
        """Unicode representation"""
        return u'%s' % (unicode(self.user))


class Tag(models.Model):
    # @TODO: instead of list_address, user list model from kittystore?
    list_address = models.CharField(max_length=50)

    # @TODO: instead of threadid, use thread model from kittystore?
    threadid = models.CharField(max_length=100)

    tag = models.CharField(max_length=255)

    def __unicode__(self):
        """Unicode representation"""
        return u'threadid = %s , tag = %s ' % (unicode(self.list_address), unicode(self.threadid))
