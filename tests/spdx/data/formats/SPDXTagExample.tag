SPDXVersion: SPDX-2.1
DataLicense: CC0-1.0
DocumentName: Sample_Document-V2.1
SPDXID: SPDXRef-DOCUMENT
DocumentNamespace: https://spdx.org/spdxdocs/spdx-example-444504E0-4F89-41D3-9A0C-0305E82C3301
DocumentComment: <text>This is a sample spreadsheet</text>

## Creation Information
Creator: Person: Gary O'Neall
Creator: Organization: Source Auditor Inc.
Creator: Tool: SourceAuditor-V1.2
Created: 2010-02-03T00:00:00Z
CreatorComment: <text>This is an example of an SPDX spreadsheet format</text>

## Review Information
Reviewer: Person: Joe Reviewer
ReviewDate: 2010-02-10T00:00:00Z
ReviewComment: <text>This is just an example.  Some of the non-standard licenses look like they are actually BSD 3 clause licenses</text>

Reviewer: Person: Suzanne Reviewer
ReviewDate: 2011-03-13T00:00:00Z
ReviewComment: <text>Another example reviewer.</text>

## Annotation Information
Annotator: Person: Jim Annotator
AnnotationType: REVIEW
AnnotationDate: 2012-03-11T00:00:00Z
AnnotationComment: <text>An example annotation comment.</text>
SPDXREF: SPDXRef-45

## Relationships
Relationship: SPDXRef-DOCUMENT DESCRIBES SPDXRef-File
Relationship: SPDXRef-DOCUMENT DESCRIBES SPDXRef-Package
Relationship: SPDXRef-DOCUMENT COPY_OF DocumentRef-spdx-tool-1.2:SPDXRef-ToolsElement
Relationship: SPDXRef-DOCUMENT CONTAINS SPDXRef-Package

## Package Information
PackageName: SPDX Translator
SPDXID: SPDXRef-Package
PackageVersion: Version 0.9.2
PackageDownloadLocation: http://www.spdx.org/tools
PackageSummary: <text>SPDX Translator utility</text>
PackageSourceInfo: <text>Version 1.0 of the SPDX Translator application</text>
PackageFileName: spdxtranslator-1.0.zip
PackageAttributionText: <text>The GNU C Library is free software.  See the file COPYING.LIB for copying conditions, and LICENSES for notices about a few contributions that require these additional notices to be distributed.  License copyright years may be listed using range notation, e.g., 1996-2015, indicating that every year in the range, inclusive, is a copyrightable year that would otherwise be listed individually.</text>
PackageSupplier: Organization:Linux Foundation
PackageOriginator: Organization:SPDX
PackageChecksum: SHA1: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12
PackageVerificationCode: 4e3211c67a2d28fced849ee1bb76e7391b93feba (SpdxTranslatorSpdx.rdf, SpdxTranslatorSpdx.txt)
PackageDescription: <text>This utility translates and SPDX RDF XML document to a spreadsheet, translates a spreadsheet to an SPDX RDF XML document and translates an SPDX RDFa document to an SPDX RDF XML document.</text>
PackageAttributionText: <text>The GNU C Library is free software.  See the file COPYING.LIB for copying conditions, and LICENSES for notices about a few contributions that require these additional notices to be distributed.  License copyright years may be listed using range notation, e.g., 1996-2015, indicating that every year in the range, inclusive, is a copyrightable year that would otherwise be listed individually.</text>
PackageComment: <text>This package includes several sub-packages.</text>

PackageCopyrightText: <text>Copyright 2010, 2011 Source Auditor Inc.</text>

PackageLicenseDeclared: (LicenseRef-3 AND LicenseRef-4 AND Apache-2.0 AND MPL-1.1 AND LicenseRef-1 AND LicenseRef-2)
PackageLicenseConcluded: (LicenseRef-3 AND LicenseRef-4 AND Apache-1.0 AND Apache-2.0 AND MPL-1.1 AND LicenseRef-1 AND LicenseRef-2)

PackageLicenseInfoFromFiles: Apache-1.0
PackageLicenseInfoFromFiles: LicenseRef-3
PackageLicenseInfoFromFiles: Apache-2.0
PackageLicenseInfoFromFiles: LicenseRef-4
PackageLicenseInfoFromFiles: LicenseRef-2
PackageLicenseInfoFromFiles: LicenseRef-1
PackageLicenseInfoFromFiles: MPL-1.1
PackageLicenseComments: <text>The declared license information can be found in the NOTICE file at the root of the archive file</text>

ExternalRef: SECURITY cpe23Type cpe:2.3:a:pivotal_software:spring_framework:4.1.0:*:*:*:*:*:*:
ExternalRefComment: <text>NIST National Vulnerability Database (NVD) describes security vulnerabilities (CVEs) which affect Vendor Product Version acmecorp:acmenator:6.6.6.</text>

## File Information
FileName: src/org/spdx/parser/DOAPProject.java
SPDXID: SPDXRef-File1
FileType: SOURCE
FileType: TEXT
FileChecksum: SHA1: 2fd4e1c67a2d28fced849ee1bb76e7391b93eB12
FileChecksum: SHA256: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb120000000000000000
LicenseConcluded: Apache-2.0
LicenseInfoInFile: Apache-2.0
FileCopyrightText: <text>Copyright 2010, 2011 Source Auditor Inc.</text>

FileName: Jenna-2.6.3/jena-2.6.3-sources.jar
SPDXID: SPDXRef-File2
FileType: ARCHIVE
FileType: OTHER
FileChecksum: SHA1: 3ab4e1c67a2d28fced849ee1bb76e7391b93f125
FileChecksum: SHA256: 3ab4e1c67a2d28fced849ee1bb76e7391b93f1250000000000000000
LicenseConcluded: LicenseRef-1
LicenseInfoInFile: LicenseRef-1
LicenseComments: <text>This license is used by Jena</text>
FileCopyrightText: <text>(c) Copyright 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009 Hewlett-Packard Development Company, LP</text>
ArtifactOfProjectName: Jena
ArtifactOfProjectHomePage: http://www.openjena.org/
ArtifactOfProjectURI: http://www.openjena.org/doap.rdf
FileComment: <text>This file belongs to Jena</text>

## Snippet Information
SnippetSPDXID: SPDXRef-Snippet
SnippetFromFileSPDXID: SPDXRef-DoapSource
SnippetLicenseComments: <text>The concluded license was taken from package xyz, from which the snippet was copied into the current file. The concluded license information was found in the COPYING.txt file in package xyz.</text>
SnippetCopyrightText: <text>Copyright 2008-2010 John Smith</text>
SnippetComment: <text>This snippet was identified as significant and highlighted in this Apache-2.0 file, when a commercial scanner identified it as being derived from file foo.c in package xyz which is licensed under GPL-2.0-or-later.</text>
SnippetName: from linux kernel
SnippetLicenseConcluded: Apache-2.0
LicenseInfoInSnippet: Apache-2.0
SnippetByteRange: 310:420

## License Information
LicenseID: LicenseRef-3
ExtractedText: <text>The CyberNeko Software License, Version 1.0

 
(C) Copyright 2002-2005, Andy Clark.  All rights reserved.
 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer. 

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in
   the documentation and/or other materials provided with the
   distribution.

3. The end-user documentation included with the redistribution,
   if any, must include the following acknowledgment:  
     "This product includes software developed by Andy Clark."
   Alternately, this acknowledgment may appear in the software itself,
   if and wherever such third-party acknowledgments normally appear.

4. The names "CyberNeko" and "NekoHTML" must not be used to endorse
   or promote products derived from this software without prior 
   written permission. For written permission, please contact 
   andyc@cyberneko.net.

5. Products derived from this software may not be called "CyberNeko",
   nor may "CyberNeko" appear in their name, without prior written
   permission of the author.

THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESSED OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR OTHER CONTRIBUTORS
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, 
OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT 
OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR 
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE 
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, 
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.</text>
LicenseName: CyberNeko License
LicenseCrossReference: http://people.apache.org/~andyc/neko/LICENSE
LicenseCrossReference: http://justasample.url.com
LicenseComment: <text>This is tye CyperNeko License</text>

LicenseID: LicenseRef-1
ExtractedText: <text>/*
 * (c) Copyright 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009 Hewlett-Packard Development Company, LP
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote products
 *    derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
 * IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 * IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 * NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 * THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */</text>

LicenseID: LicenseRef-2
ExtractedText: <text>This package includes the GRDDL parser developed by Hewlett Packard under the following license:
© Copyright 2007 Hewlett-Packard Development Company, LP

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met: 

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. 
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution. 
The name of the author may not be used to endorse or promote products derived from this software without specific prior written permission. 
THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. </text>

LicenseID: LicenseRef-4
ExtractedText: <text>/*
 * (c) Copyright 2009 University of Bristol
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote products
 *    derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
 * IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 * IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 * NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 * THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */  </text>

