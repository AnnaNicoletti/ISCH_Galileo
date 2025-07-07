<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tei="http://www.tei-c.org/ns/1.0"
                exclude-result-prefixes="tei">
    
    <xsl:template match="/">
        <html>
            <head>
                <style>
                    /* Stile base per la tabella */
                    table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 1em;
                    font-family: Arial, sans-serif;
                    }
                    th, td {
                    border: 1px solid #666;
                    padding: 8px 12px;
                    text-align: left;
                    }
                    th {
                    background-color: #eee;
                    }
                    tr:nth-child(even) {
                    background-color: #f9f9f9;
                    }
                    /* Stile per il titolo */
                    h2 {
                    font-family: 'Georgia', serif;
                    margin-bottom: 0.5em;
                    }
                </style>
            </head>
            <body>
                <!--Title-->
                <h2><xsl:value-of select="/tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/></h2>
                <!--Title-->
                
                <!--Metadata Table-->
                <table>
                    <tr>
                        <th>Metadata</th>
                        <th>Values</th>
                        <th>Authority Control</th>
                    </tr>
                    <tr>
                        <td>Author</td>
                        <td>
                            <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:author/tei:persName/tei:forename"/>
                            <xsl:text> </xsl:text>
                            <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:author/tei:persName/tei:surname"/>
                        </td>
                        <td>
                            <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:author/tei:persName/tei:idno[@type='VIAF']"/>
                        </td>
                    </tr>
                    <tr>
                        <td>Date</td>
                        <td>
                            <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:date/@when"/>
                        </td>
                        <td></td>
                    </tr>
                    <tr>
                        <td>Edition</td>
                        <td>
                            <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:fileDesc/tei:editionStmt/tei:edition/tei:title"/>
                        </td>
                        <td></td>
                    </tr>
                    <tr>
                        <td>Publisher</td>
                        <td>
                            <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:publisher"/>
                        </td>
                        <td>
                            <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:pubPlace"/>
                        </td>
                    </tr>
                    <tr>
                        <td>Licence</td>
                        <td colspan="2">
                            <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:availability/tei:licence"/>
                            <xsl:text> (</xsl:text>
                            <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:availability/tei:licence/@target"/>
                            <xsl:text>)</xsl:text>
                        </td>
                    </tr>
                </table>
                <!--Metadata Table-->
                
                <!--Text-->
                <div>
                    <!--First Chapter-->
                    
                    <!--Title-->
                    <h4>
                        <xsl:value-of select="/tei:TEI/tei:text/tei:body/tei:div[@type='chapter']/tei:head"/>
                    </h4>
                    
                    <!-- Itera solo sui dialoghi dentro l’unico capitolo -->
                    <xsl:for-each select="/tei:TEI/tei:text/tei:body/tei:div[@type='chapter']/tei:div[@type='dialogue']">
                        <p>
                            <strong><xsl:value-of select="tei:speaker"/></strong>
                            <xsl:text>: </xsl:text>
                            <xsl:value-of select="tei:p"/>
                        </p>
                    </xsl:for-each>
                    
                    
                    <!--First Chapter-->
                </div>
                <!--Text-->
            </body>
        </html>
        
    </xsl:template>
    
</xsl:stylesheet>
