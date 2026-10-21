# BardBox UID Registry (redirect)

Retired as a separate guide on October 19, 2026
([bardbox#31 decision entry](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269561991)).
Its former "authoritative Google Sheets" link was an unfilled placeholder, so no
shared spreadsheet is authoritative.

- **UID format, immutability, no reuse of retired UIDs, labelling, legacy IDs and
  status values:** [Node naming standard](node-naming-standard.md).
- **Who owns node definitions and entity association:** the project Registry in the
  [Architecture Map](architecture-map.md#project-server-template).
- **Shared allocation, enrollment and authentication:** deferred registry work in
  [bardbox#10](https://github.com/bardphysicslab/bardbox/issues/10) (one Registry authority per project instance,
  [REG-AUTHORITY-1](https://github.com/bardphysicslab/bardbox/issues/10#issuecomment-6313633845));
  [firmware-tools#41](https://github.com/bardphysicslab/firmware-tools/issues/41) is superseded history.

Where the UID lives today: programmable nodes provisioned over USB keep it in
their device configuration record
([USB device configuration](usb-device-configuration-standard.md#2-device-configuration-records));
older builds compile it in. Non-programmable instruments receive their UID in
server driver configuration.
