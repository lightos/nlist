import os
import xml.etree.ElementTree


e = xml.etree.ElementTree.parse(r'samples.xml').getroot()

target = "netbios-ssn"
directory = "samples"
found = []

if not os.path.exists(directory):
    os.makedirs(directory)

for host in e.findall('host'):
    if host[0].attrib["state"] != "up":
        continue
    addr = host[1].attrib["addr"]
    for ports in  host.findall('ports'):
        for port in ports.findall('port'):
            if port[0].attrib["state"] != "open": # port filtered/closed
                break
            portid = port.attrib["portid"]
            for service in port:
                if service.get('name') and target in service.get('name'):
                    found.append({"Address":addr+":"+portid,
                                  "Service": (service.get('name'),
                                              service.get('product'))})
                    # file_ = "%s\\%s%s.txt" % (directory, target, portid)
                    file_ = "%s\\%s.txt" % (directory, target)
                    with open(file_, 'a') as output:
                        output.write("%s:%s\r\n" % (addr, portid)) # hydra

print found
