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

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

from local import rally_rest

class Rally(callbacks.PluginRegexp):
    """
    Add the help for "@plugin help Rally" here
    This should describe *how* to use this plugin.
    """
    threaded = True
    regexps = ['rallyIdSnarfer']
    
    # {{{ rallyIdSnarfer
    def rallyIdSnarfer(self, irc, msg, match):
        r'(DE\d{4}|US\d{5}|TA\d{6})'
        
        channel = irc.channel
        
        if not irc.isChannel(channel):
            return
        
        if self.registryValue('snarfRallyIDs', channel):
            rallyId = match.group(0)
            
            artifact_type = 'artifact'
            
            if rallyId[:2] == 'US':
                artifact_type = 'HierarchicalRequirement'
            elif rallyId[:2] == 'TA':
                artifact_type = 'Task'
            elif rallyId[:2] == 'DE':
                artifact_type = 'Defect'
            
            try:
                rq = rally_rest.RallyQuery(
                    self.registryValue('rallyUserId'),
                    self.registryValue('rallyPassword')
                )
                
                artifact = rq.findArtifactByFormattedId(rallyId, artifact_type)
                
                maybe_blocked = ""
                
                if u'Blocked' in artifact and artifact[u'Blocked']:
                    maybe_blocked = ", Blocked"
                
                if artifact[u'_type'] in (u'Task',):
                    state = artifact[u'State']
                elif artifact[u'_type'] in (u'HierarchicalRequirement', u'Defect'):
                    state = artifact[u'ScheduleState']
                
                reply_msg = u"[%s] %s ⪼ (%s%s)" % (rallyId, artifact[u'Name'], state, maybe_blocked)
                
                irc.reply(reply_msg, prefixNick = False, notice = True)
            except rally_rest.RallyError, e:
                self.log.error("unable to look up %s", rallyId, exc_info = True)
            
        
    
    rallyIdSnarfer = urlSnarfer(rallyIdSnarfer)
    # }}}
    
    


Class = Rally


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
