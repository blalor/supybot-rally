# encoding: utf-8
###
# Copyright (c) 2011, Brian Lalor
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

from supybot.test import *

class RallyTestCase(ChannelPluginTestCase):
    plugins = ('Rally',)
    timeout = 2
    
    def setUp(self):
        ChannelPluginTestCase.setUp(self)
        
        conf.supybot.plugins.Rally.rallyUserId.setValue("brian.lalor@pearson.com")
        conf.supybot.plugins.Rally.rallyPassword.setValue("password")
    
    
    def testUserStory(self):
        """checks that a valid user story title is looked up"""
        
        try:
            conf.supybot.plugins.Rally.snarfRallyIDs.setValue(True)
            self.assertSnarfResponse('US42859',
                                     '[US42859] Access Code Self-Reg handoff to Localizations team ⪼ (In-Progress)')
                                     
        
        finally:
            conf.supybot.plugins.Rally.snarfRallyIDs.setValue(False)
    
    
    def testUserStoryInline(self):
        """checks that a valid user story title is looked up"""
        
        try:
            conf.supybot.plugins.Rally.snarfRallyIDs.setValue(True)
                                     
            self.assertSnarfResponse('yo, dawg, i heard you like user stories in your user stories so i added a user story to your US40312 user story',
                                     '[US40312] RADmin: CreateUser screen - Modification (UI+Service) ⪼ (In-Progress)')
        
        finally:
            conf.supybot.plugins.Rally.snarfRallyIDs.setValue(False)
    
    
    def testDefect(self):
        """checks that a valid defect title is looked up"""
        
        try:
            conf.supybot.plugins.Rally.snarfRallyIDs.setValue(True)
            self.assertSnarfResponse('DE9395',
                                     '[DE9395] CAS: Consenting to license agreement or Resetting password results in System error ⪼ (Defined)')
        
        finally:
            conf.supybot.plugins.Rally.snarfRallyIDs.setValue(False)
    
    
    def testBlockedDefect(self):
        """checks that a valid defect title is looked up"""
        
        try:
            conf.supybot.plugins.Rally.snarfRallyIDs.setValue(True)
            self.assertSnarfResponse('DE8977',
                                     '[DE8977] Access Code Self Reg: UI is not rendered properly when the labels or links exceed a certain length ⪼ (Backlog, Blocked)')
        
        finally:
            conf.supybot.plugins.Rally.snarfRallyIDs.setValue(False)
    
    
    def testTask(self):
        """checks that a valid task title is looked up"""
        
        try:
            conf.supybot.plugins.Rally.snarfRallyIDs.setValue(True)
            self.assertSnarfResponse('TA123205',
                                     '[TA123205] SQE - Test Planning and Design ⪼ (Defined)')
        
        finally:
            conf.supybot.plugins.Rally.snarfRallyIDs.setValue(False)
    



# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
