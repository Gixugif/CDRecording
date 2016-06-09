#!/usr/bin/python
# -*- coding: utf-8 -*-
# Title: Call_Detail_Record
# Description: Class for one
# CDR
# separately.
# Date: 2/2/15
# Author: Jeffrey Zic

class Call_Detail_Record:

    """ Call Detail Records contain metadata for phone calls."""

    def __init__(self):
        self.bbx_cdr_id = ('', )
        self.network_addr = ('', )
        self.bbx_fax_inbound_id = ('', )
        self.billsec = ('', )
        self.original_callee_id_name = ('', )
        self.end_timestamp = ('', )
        self.direction = ('', )
        self.destination_name = ('', )
        self.transfer_source = ('', )
        self.original_callee_id_number = ('', )
        self.write_rate = ('', )
        self.transfer_to = ('', )
        self.write_codec = ('', )
        self.context = ('', )
        self.callee_bbx_phone_id = ('', )
        self.destination_number = ('', )
        self.caller_id_number = ('', )
        self.caller_bbx_phone_registration_id = ('', )
        self.hangup_cause = ('', )
        self.original_caller_id_number = ('', )
        self.gateway_name = ('', )
        self.record_file_name = ('', )
        self.callee_bbx_user_id = ('', )
        self.record_file_checksum = ('', )
        self.caller_bbx_phone_id = ('', )
        self.duration = ('', )
        self.callee_bbx_phone_registration_id = ('', )
        self.answer_timestamp = ('', )
        self.hangup_originator = ('', )
        self.transfer_history = ('', )
        self.call_type = ('', )
        self.source_table = ('', )
        self.bbx_queue_id = ('', )
        self.hold_events = ('', )
        self.start_timestamp = ('', )
        self.uuid = ('', )
        self.record_keep_days = ('', )
        self.bbx_fax_outbound_id = ('', )
        self.bleg_uuid = ('', )
        self.bbx_callflow_id = ('', )
        self.destination_list = ('', )
        self.caller_id_name = ('', )
        self.click_to_call_uuid = ('', )
        self.read_rate = ('', )
        self.original_caller_id_name = ('', )
        self.recording_retention = ('', )
        self.caller_bbx_user_id = ('', )
        self.destination_type = ('', )
        self.outbound_route = ('', )
        self.processed = ('', )
        self.accountcode = ('', )
        self.read_codec = ''
