# Document Information

SPDXVersion: SPDX-2.2
DataLicense: CC0-1.0
DocumentNamespace: http://spdx.org/spdxdocs/spdx-document-xyz
DocumentName: xyz-0.1.0
SPDXID: SPDXRef-DOCUMENT


# Creation Info

Creator: Organization: Example Inc.
Creator: Person: Thomas Steenbergen
Created: 2020-07-23T18:30:22Z


# Relationships

Relationship: SPDXRef-Package-xyz CONTAINS SPDXRef-Package-curl
Relationship: SPDXRef-Package-xyz CONTAINS SPDXRef-Package-openssl


# Package

PackageName: xyz
SPDXID: SPDXRef-Package-xyz
PackageVersion: 0.1.0
PackageDownloadLocation: git+ssh://gitlab.example.com:3389/products/xyz.git@b2c358080011af6a366d2512a25a379fbe7b1f78
FilesAnalyzed: False
PackageSummary: <text>Awesome product created by Example Inc.</text>
PackageLicenseDeclared: (Apache-2.0 AND curl AND LicenseRef-Proprietary-ExampleInc)
PackageLicenseConcluded: NOASSERTION
PackageCopyrightText: <text>copyright 2004-2020 Example Inc. All Rights Reserved.</text>
PackageHomePage: https://example.com/products/xyz


# Package

PackageName: curl
SPDXID: SPDXRef-Package-curl
PackageVersion: 7.70.0
PackageDownloadLocation: https://github.com/curl/curl/releases/download/curl-7_70_0/curl-7.70.0.tar.gz
FilesAnalyzed: False
PackageFileName: ./libs/curl
PackageDescription: <text>A command line tool and library for transferring data with URL syntax, supporting HTTP, HTTPS, FTP, FTPS, GOPHER, TFTP, SCP, SFTP, SMB, TELNET, DICT, LDAP, LDAPS, MQTT, FILE, IMAP, SMTP, POP3, RTSP and RTMP. libcurl offers a myriad of powerful features.</text>
PackageLicenseDeclared: curl
PackageLicenseConcluded: NOASSERTION
PackageCopyrightText: <text>Copyright (c) 1996 - 2020, Daniel Stenberg, <daniel@haxx.se>, and many contributors, see the THANKS file.</text>
PackageHomePage: https://curl.haxx.se/


# Package

PackageName: openssl
SPDXID: SPDXRef-Package-openssl
PackageVersion: 1.1.1g
PackageDownloadLocation: git+ssh://github.com/openssl/openssl.git@e2e09d9fba1187f8d6aafaa34d4172f56f1ffb72
FilesAnalyzed: False
PackageFileName: ./libs/openssl
PackageDescription: <text>OpenSSL is a robust, commercial-grade, full-featured Open Source Toolkit for the Transport Layer Security (TLS) protocol formerly known as the Secure Sockets Layer (SSL) protocol. The protocol implementation is based on a full-strength general purpose cryptographic library, which can also be used stand-alone.</text>
PackageLicenseDeclared: Apache-2.0
PackageLicenseConcluded: NOASSERTION
PackageCopyrightText: <text>copyright 2004-2020 The OpenSSL Project Authors. All Rights Reserved.</text>
PackageHomePage: https://www.openssl.org/
