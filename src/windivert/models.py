# -*- coding: utf-8 -*-
# Copyright (C) 2013  Fabio Falcinelli
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from binascii import unhexlify, hexlify

__author__ = 'fabio'

import ctypes
import struct


int_to_port = lambda x: sum([ord(x) * (256 ** i) for i, x in enumerate(struct.pack(">H", x))])
int_to_ipv4 = lambda x: ".".join([str(x) for x in map(ord, struct.pack("<I", x))])


#TODO simplify for readability...
def int_to_ipv6(addr):
    out = []
    for i in addr:
        ipv6_tokens = [hex(ord(x)).rstrip("L").lstrip("0x").zfill(2) for x in struct.pack("<H", i)]
        out.append(["".join([a, b]) for a, b in zip(ipv6_tokens[::2], ipv6_tokens[1::2])][0])
    return ":".join(out)


def format_structure(instance):
    """
    Return a string representation for the structure
    """
    if hasattr(instance, "_fields_"):
        out = []
        for field in instance._fields_:
            out.append("[%s: %s]" % (field[0], getattr(instance, field[0], None)))
        return "".join(out)
    else:
        raise ValueError("Passed argument is not a structure!")


class DivertAddress(ctypes.Structure):
    """
    Ctypes Structure for DIVERT_ADDRESS.
    The DIVERT_ADDRESS structure represents the "address" of a captured or injected packet.
    The address includes the packet's network interfaces and the packet direction.

    typedef struct
    {
        UINT32 IfIdx;
        UINT32 SubIfIdx;
        UINT8  Direction;
    } DIVERT_ADDRESS, *PDIVERT_ADDRESS;
    """
    _fields_ = [("IfIdx", ctypes.c_uint32), # The interface index on which the packet arrived
                ("SubIfIdx", ctypes.c_uint32), # The sub-interface index for IfIdx.
                ("Direction", ctypes.c_uint8)]  # The packet's direction. The possible values are

    def __str__(self):
        return format_structure(self)


class DivertIpHeader(ctypes.Structure):
    """
    Ctypes structure for DIVERT_IPHDR: IPv4 header definition.

    typedef struct
    {
        UINT8  HdrLength:4;
        UINT8  Version:4;
        UINT8  TOS;
        UINT16 Length;
        UINT16 Id;
        UINT16 ...; --> FragOff0
        UINT8  TTL;
        UINT8  Protocol;
        UINT16 Checksum;
        UINT32 SrcAddr;
        UINT32 DstAddr;
    } DIVERT_IPHDR, *PDIVERT_IPHDR;
    """
    _fields_ = [("HdrLength", ctypes.c_uint8, 4),
                ("Version", ctypes.c_uint8, 4),
                ("TOS", ctypes.c_uint8),
                ("Length", ctypes.c_uint16),
                ("Id", ctypes.c_uint16),
                ("FragOff0", ctypes.c_uint16),
                ("TTL", ctypes.c_uint8),
                ("Protocol", ctypes.c_uint8),
                ("Checksum", ctypes.c_uint16),
                ("SrcAddr", ctypes.c_uint32),
                ("DstAddr", ctypes.c_uint32)]

    def __str__(self):
        return format_structure(self)


#TODO: adjust fields to code instead of documentation
class DivertIpv6Header(ctypes.Structure):
    """
    Ctypes structure for DIVERT_IPV6HDR: IPv6 header definition.

    UINT8  TrafficClass0:4;
    UINT8  Version:4;
    UINT8  FlowLabel0:4;
    UINT8  TrafficClass1:4;
    UINT16 FlowLabel1;

    typedef struct
    {
        UINT32 Version:4;
        UINT32 ...:28;
        UINT16 Length;
        UINT8  NextHdr;
        UINT8  HopLimit;
        UINT32 SrcAddr[4];
        UINT32 DstAddr[4];
    } DIVERT_IPV6HDR, *PDIVERT_IPV6HDR;
    """
    _fields_ = [("TrafficClass0", ctypes.c_uint8, 4),
                ("Version", ctypes.c_uint8, 4),
                ("FlowLabel0", ctypes.c_uint8, 4),
                ("TrafficClass1", ctypes.c_uint8, 4),
                ("FlowLabel1", ctypes.c_uint16, 4),
                ("Length", ctypes.c_uint16),
                ("NextHdr", ctypes.c_uint8),
                ("HopLimit", ctypes.c_uint8),
                ("SrcAddr", ctypes.c_uint32 * 4),
                ("DstAddr", ctypes.c_uint32 * 4), ]

    def __str__(self):
        return format_structure(self)


class DivertIcmpHeader(ctypes.Structure):
    """
    Ctypes structure for DIVERT_ICMPHDR: ICMP header definition.

    typedef struct
    {
        UINT8  Type;
        UINT8  Code;
        UINT16 Checksum;
        UINT32 Body;
    } DIVERT_ICMPHDR, *PDIVERT_ICMPHDR;
    """
    _fields_ = [("Type", ctypes.c_uint8),
                ("Code", ctypes.c_uint8),
                ("Checksum", ctypes.c_uint16),
                ("Body", ctypes.c_uint32)]

    def __str__(self):
        return format_structure(self)


class DivertIcmpv6Header(ctypes.Structure):
    """
    Ctypes structure for DIVERT_IPV6HDR: ICMPv6 header definition.

    typedef struct
    {
        UINT8  Type;
        UINT8  Code;
        UINT16 Checksum;
        UINT32 Body;
    } DIVERT_ICMPV6HDR, *PDIVERT_ICMPV6HDR;
    """
    _fields_ = [("Type", ctypes.c_uint8),
                ("Code", ctypes.c_uint8),
                ("Checksum", ctypes.c_uint16),
                ("Body", ctypes.c_uint32)]

    def __str__(self):
        return format_structure(self)


class DivertTcpHeader(ctypes.Structure):
    """
    Ctypes structure for DIVERT_TCPHDR: TCP header definition.

    typedef struct
    {
        UINT16 SrcPort;
        UINT16 DstPort;
        UINT32 SeqNum;
        UINT32 AckNum;
        UINT16 Reserved1:4;
        UINT16 HdrLength:4;
        UINT16 Fin:1;
        UINT16 Syn:1;
        UINT16 Rst:1;
        UINT16 Psh:1;
        UINT16 Ack:1;
        UINT16 Urg:1;
        UINT16 Reserved2:2;
        UINT16 Window;
        UINT16 Checksum;
        UINT16 UrgPtr;
    } DIVERT_TCPHDR, *PDIVERT_TCPHDR;
    """
    _fields_ = [("SrcPort", ctypes.c_uint16),
                ("DstPort", ctypes.c_uint16),
                ("SeqNum", ctypes.c_uint32),
                ("AckNum", ctypes.c_uint32),
                ("Reserved1", ctypes.c_uint16, 4),
                ("HdrLength", ctypes.c_uint16, 4),
                ("Fin", ctypes.c_uint16, 1),
                ("Syn", ctypes.c_uint16, 1),
                ("Rst", ctypes.c_uint16, 1),
                ("Psh", ctypes.c_uint16, 1),
                ("Ack", ctypes.c_uint16, 1),
                ("Urg", ctypes.c_uint16, 1),
                ("Reserved2", ctypes.c_uint16, 2),
                ("Window", ctypes.c_uint16),
                ("Checksum", ctypes.c_uint16),
                ("UrgPtr", ctypes.c_uint16)]

    def __str__(self):
        return format_structure(self)


class DivertUdpHeader(ctypes.Structure):
    """
    Ctypes structure for DIVERT_UDPHDR: UDP header definition.

    typedef struct
    {
        UINT16 SrcPort;
        UINT16 DstPort;
        UINT16 Length;
        UINT16 Checksum;
    } DIVERT_UDPHDR, *PDIVERT_UDPHDR;
    """
    _fields_ = [("SrcPort", ctypes.c_uint16),
                ("DstPort", ctypes.c_uint16),
                ("Length", ctypes.c_uint16),
                ("Checksum", ctypes.c_uint16)]

    def __str__(self):
        return format_structure(self)


class CapturedMetadata(object):
    """
    Captured metadata on interface and flow direction
    """

    def __init__(self, iface, direction):
        self.iface = iface
        self.direction = direction

    def __str__(self):
        return "Interface: (Index: %s, SubIndex %s) Flow: %s" % (self.iface[0],
                                                                 self.iface[1],
                                                                 "outbound" if self.direction != 1 else "inbound")


class CapturedPacket(object):
    """
    Gathers several network layers of data
    """
    #TODO: changes to attributes reflecting to raw_packet would be cool :-)

    def __init__(self, net_hdr=None, tran_hdr=None, content=None, raw_packet=None):
        self.content = content
        self.raw_packet = raw_packet
        self.src_addr, self.src_port = None, None
        self.dst_addr, self.dst_port = None, None
        self.raw_net_hdr, self.raw_tran_hdr = None, None
        if net_hdr:
            self.set_network_header(net_hdr)
        if tran_hdr:
            self.set_transport_header(tran_hdr)

    def set_network_header(self, header):
        self.raw_net_hdr = header
        if hasattr(header, "SrcAddr"):
            self.src_addr = int_to_ipv4(header.SrcAddr)
        if hasattr(header, "DstAddr"):
            self.dst_addr = int_to_ipv4(header.DstAddr)

    def set_transport_header(self, header):
        self.raw_tran_hdr = header
        if hasattr(header, "SrcPort"):
            self.src_port = int_to_port(header.SrcPort)
        if hasattr(header, "DstPort"):
            self.dst_port = int_to_port(header.DstPort)

    def to_raw_packet(self):
        hexed = hexlify(self.raw_packet)
        headers = hexlify(self.raw_net_hdr)+hexlify(self.raw_tran_hdr)
        return unhexlify(headers+hexed[len(headers):])

    def __str__(self):
        return "Packet from %s to %s [%s]" % ("%s:%s" % (self.src_addr, self.src_port),
                                              "%s:%s" % (self.dst_addr, self.dst_port),
                                              self.content)


