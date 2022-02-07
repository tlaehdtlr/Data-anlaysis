import io
import sys
from datetime import datetime

from pcapng import FileScanner
from pcapng.blocks import EnhancedPacket, Packet, SimplePacket, InterfaceDescription, SectionHeader

import numpy as np

def col256(text, fg=None, bg=None, bold=False):
    def _get_color(col):
        return "8;5;{0:d}".format(_to_color(col))

    def _to_color(num):
        if isinstance(num, int):
            return num  # Assume it is already a color

        if isinstance(num, str) and len(num) <= 3:
            return 16 + int(num, 6)

        raise ValueError("Invalid color: {0!r}".format(num))

    if not isinstance(text, str):
        text = repr(text)

    buf = io.StringIO()

    if bold:
        buf.write("\x1b[1m")

    if fg is not None:
        buf.write("\x1b[3{0}m".format(_get_color(fg)))

    if bg is not None:
        buf.write("\x1b[4{0}m".format(_get_color(bg)))

    buf.write(text)
    buf.write("\x1b[0m")
    return buf.getvalue()

def dump_information(scanner):
    for block in scanner:
        if isinstance(block, SectionHeader):
            pprint_sectionheader(block)
        elif isinstance(block, InterfaceDescription):
            pprint_interfacedesc(block)
        elif isinstance(block, EnhancedPacket):
            pprint_enhanced_packet(block)
        else:
            print("    " + str(block))


def pprint_options(options):
    if len(options):
        yield "--"
        for key, values in options.iter_all_items():
            for value in values:
                yield col256(key + ":", bold=True, fg="453")
                yield col256(str(value), fg="340")


def pprint_sectionheader(block):
    endianness_desc = {
        "<": "Little endian",
        ">": "Big endian",
        "!": "Network (Big endian)",
        "=": "Native",
    }

    text = [
        col256(" Section ", bg="400", fg="550"),
        col256("version:", bold=True),
        col256(".".join(str(x) for x in block.version), fg="145"),
        # col256('endianness:', bold=True),
        "-",
        col256(endianness_desc.get(block.endianness, "Unknown endianness"), bold=True),
        "-",
    ]

    if block.length < 0:
        text.append(col256("unspecified size", bold=True))
    else:
        text.append(col256("length:", bold=True))
        text.append(col256(str(block.length), fg="145"))

    text.extend(pprint_options(block.options))
    print(" ".join(text))


def pprint_interfacedesc(block):
    text = [
        col256(" Interface #{0} ".format(block.interface_id), bg="010", fg="453"),
        col256("Link type:", bold=True),
        col256(str(block.link_type), fg="140"),
        col256(block.link_type_description, fg="145"),
        col256("Snap length:", bold=True),
        col256(str(block.snaplen), fg="145"),
    ]
    text.extend(pprint_options(block.options))
    print(" ".join(text))


def pprint_enhanced_packet(block):
    text = [
        col256(" Packet+ ", bg="001", fg="345"),
        # col256('NIC:', bold=True),
        # col256(str(block.interface_id), fg='145'),
        col256(str(block.interface.options["if_name"]), fg="140"),
        col256(
            str(
                datetime.utcfromtimestamp(block.timestamp).strftime("%Y-%m-%d %H:%M:%S")
            ),
            fg="455",
        ),
    ]
    try:
        text.extend(
            [
                col256("NIC:", bold=True),
                col256(block.interface_id, fg="145"),
                col256(block.interface.options["if_name"], fg="140"),
            ]
        )
    except KeyError:
        pass

    text.extend(
        [
            # col256('Size:', bold=True),
            col256(str(block.packet_len) + " bytes ", fg="025")
        ]
    )

    if block.captured_len != block.packet_len:
        text.extend(
            [
                col256("Truncated to:", bold=True),
                col256(str(block.captured_len) + "bytes", fg="145"),
            ]
        )

    text.extend(pprint_options(block.options))
    print(" ".join(text))

    if block.interface.link_type == 1:
        # print(repr(block.packet_data))
        # print(col256(repr(Ether(block.packet_data)), fg='255'))

        _info = format_packet_information(block.packet_data)
        print("\n".join("    " + line for line in _info))

    else:
        print("        Printing information for non-ethernet packets")
        print("        is not supported yet.")

    # print('\n'.join('        ' + line
    #                 for line in format_binary_data(block.packet_data)))


def format_packet_information(packet_data):
    decoded = Ether(packet_data)
    return format_scapy_packet(decoded)


def format_scapy_packet(packet):
    fields = []
    for f in packet.fields_desc:
        # if isinstance(f, ConditionalField) and not f._evalcond(self):
        #     continue
        if f.name in packet.fields:
            val = f.i2repr(packet, packet.fields[f.name])

        elif f.name in packet.overloaded_fields:
            val = f.i2repr(packet, packet.overloaded_fields[f.name])

        else:
            continue

        fields.append("{0}={1}".format(col256(f.name, "542"), col256(val, "352")))

    yield "{0} {1}".format(col256(packet.__class__.__name__, "501"), " ".join(fields))

    if packet.payload:
        if isinstance(packet.payload, scapy.packet.Raw):
            raw_data = str(packet.payload)
            for line in make_printable(raw_data).splitlines():
                yield "    " + line

            #     for line in format_binary_data(raw_data):
            #         yield '    ' + line

        elif isinstance(packet.payload, scapy.packet.Packet):
            for line in format_scapy_packet(packet.payload):
                yield "    " + line

        else:
            for line in repr(packet.payload).splitlines():
                yield "    " + line


twos_complement = 128<<16   # MSB 1000 0000
def convert_twos_comple(value):
    if value&twos_complement:
        # negative
        value = -(2**24 - value)

    return value


PACKET_TYPES = EnhancedPacket, Packet, SimplePacket
def read_sniffer_raw_data(packets, cnt):
    file_name = "sniffer_raw_data/sniffer_test_signal.pcapng"
    # file_name = "sniffer_raw_data/yeom_sniffer_183F.pcapng"
    print("file name : ", file_name)
    print("")
    with open(file_name, 'rb') as fp:
        scanner = FileScanner(fp)
        test = 0

        for block in scanner:
            test+=1
            # print(dir(block))
            # return ;
            if not (test in list(range(4050,4064))): continue
            if (block.packet_len == 26): continue
            print("No. ", test - 2)
            print(block.packet_payload_info)
            print("")
            print(block.packet_len, block.packet_data)
            print("")
            if not (100< test < 500): continue
            if isinstance(block, EnhancedPacket):
                print(block.packet_payload_info, block.packet_payload_info)

                # if block.packet_len == 267:
                #     cnt+=1
                #     # if not (cnt == 4): continue
                #     packets.append(list(map(int, block.packet_data))[30:264])


gain = 24
lsb_size = 2*(2.048 -  (-2.5)) / gain / (2**24 - 1) # scale : V
def dac_data(dac_arr, packet_decimal):
    data = []
    for ch in range(19):
        val = packet_decimal[ch*3]<<16 | packet_decimal[ch*3+1]<<8 | packet_decimal[ch*3+2]
        val = convert_twos_comple(val)
        val = val * lsb_size * gain * 10**6
        data.append(val)
    dac_arr.append(data)
    return ;


def save_txt(data):
    ouput_filename = "test_sniffer_data_processed.txt"
    # ouput_filename = "183F_sniffer_data_processed.txt"
    np.savetxt(ouput_filename , data, delimiter=',', newline='\n')
    return ;


def main():
    print(" ======================================= sniffer data converter  ===========================================")

    cnt = 0
    packets = []
    read_sniffer_raw_data(packets, cnt);

    dac_arr = []
    for packet in packets:
        dac_data(dac_arr, packet)

    np_data = np.array(dac_arr)
    # print(np_data[:,0].size)
    # save_txt(np_data)
    # for i in range(cnt):
    #     if 5<i<10:
    #         print(a[i])

main()