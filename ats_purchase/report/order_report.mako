<html>
<head>
    <style type="text/css">
        ${css}
         .note{
               margin-top: 10px;
               margin-bottom: 10px;
               font-size:12px;
               text-align:left;
            }

    </style>
</head>
<body>
    </br>
    </br>
    </br>
    </br>
    </br>
    </br>
     %for o in objects :
        <% setLang(o.partner_id.lang) %>
        <table class="basic_table"  style="display: inline-block; float: left; margin-left:0; text-align:left;" width="45%" height=80px>
            <tr>
                <td width='1%' style="background-color:#003366; color:white; ">
                    ${'V'}
                    ${'E'}
                    ${'N'}
                    ${'D'}
                    ${'O'}
                    ${'R'}
                </td >
                <td width='44%'>
                    ${o.partner_id and o.partner_id.title and o.partner_id.title.name or '' | entity}
                    ${o.partner_id and o.partner_id.name or ''| entity}</br>
                    ${o.partner_id.street or ''|entity}</br>
                    %if o.partner_id.street2:
                        ${o.partner_id.street or ''|entity}</br>
                    %endif
                    %if o.partner_id.zip:
                        ${o.partner_id.zip or ''|entity}
                    %endif
                    %if o.partner_id.city:
                        ${o.partner_id.city or ''|entity}</br>
                    %endif
                    %if o.partner_id.country_id:
                        ${o.partner_id.country_id.name or ''|entity}</br>
                    %endif
                   %if o.partner_id.phone :
                        ${_("Tel")}: ${o.partner_id.phone or ''|entity}</br>
                   %endif
                   %if o.partner_id.fax :
                        ${_("Fax")}: ${o.partner_id.fax or ''|entity}</br>
                   %endif
                   %if o.partner_id.email :
                       ${_("E-mail")}: ${o.partner_id.email or ''|entity}</br>
                   %endif
                </td>
            </tr>
        </table>
        <table class="basic_table" align="right" style="display: inline-block; float: right; margin-right:0px; text-align:left;" " width="45%" height=80px>
            <tr>
                <td width='1%' style="background-color:#003366; font-align:center; color:white; ">
                    ${'S'}
                    ${'H'}
                    ${'I'}
                    ${'P'}
                    ${''}
                    ${'T'}
                    ${'O'}
                </td >
                <td width='44%'>
                    ${o.dest_address_id and o.dest_address_id.name or o.warehouse_id and o.warehouse_id.name or '' | entity}</br>
                    ${o.dest_address_id.street or o.warehouse_id.partner_id.street or ''|entity}</br>
                    %if o.dest_address_id.street2 or o.warehouse_id.partner_id.street2:
                        ${o.dest_address_id.street2 or o.warehouse_id.partner_id.street2 or ''|entity}</br>
                    %endif
                    %if o.dest_address_id.zip or o.warehouse_id.partner_id.zip:
                        ${o.dest_address_id.zip or o.warehouse_id.partner_id.zip or ''|entity}
                    %endif
                    %if o.dest_address_id.city or o.warehouse_id.partner_id.city:
                        ${o.dest_address_id.city or o.warehouse_id.partner_id.zip or''|entity}</br>
                    %endif
                    %if o.dest_address_id.country_id or o.warehouse_id.partner_id.country_id :
                        ${o.dest_address_id.country_id.name or o.warehouse_id.partner_id.country_id or ''|entity}</br>
                    %endif
                   %if o.dest_address_id.phone or o.warehouse_id.partner_id.phone:
                        ${_("Tel")}: ${o.dest_address_id.phone or o.warehouse_id.partner_id.phone or ''|entity}</br>
                    %endif
                   %if o.dest_address_id.fax or o.warehouse_id.partner_id.fax:
                        ${_("Fax")}: ${o.dest_address_id.fax or o.warehouse_id.partner_id.fax or ''|entity}</br>
                   %endif
                   %if o.dest_address_id.email or o.warehouse_id.partner_id.email:
                        ${_("E-mail")}: ${o.dest_address_id.email or o.warehouse_id.partner_id.email or ''|entity}</br>
                   %endif
                </td>
            </tr>
        </table>
        <br/><br/><br/><br/><br/><br/>
        <table class="basic_table" style=" border:1px solid #003366; margin-left:0;color:#003366;background-color:#99CCCC;" width="100%" height=80px>
            <tr>
                <td width="60%" style="border-style:none;text-align:left;padding-left:30px; ">
                    <b>${'DELIVERY DATE'}</b>
                </td>
                <td width="40%" style="border-style:none;text-align:left;">
                    <b>${'TERMS'}</b>
                </td>
            </tr>
            <tr>
                <td width="60%" style="border-style:none;text-align:left;padding-left:30px; ">
                    <b>${'REQUESTED BY'}</b>
                </td>
                <td width="40%" style="border-style:none;text-align:left;">
                    <b>${'SHIPPER'}</b>
                </td>
            </tr>
            <tr>
                <td width="60%" style="border-style:none;text-align:left;padding-left:80px; ">
                    <b>${'NOTES'}</b>
                </td>
                <td width="40%" style="border-style:none;text-align:left;">
                </td>
            </tr>
        </table>
        <br/><br/><br/>
        <table class="basic_table"  style=" color:#003366; padding-top:0px; margin-top:0; margin-left:0; text-align:center;" width="100%">
        <tr>
            <td width="10%" style="font-size:11;">
                <b>${'QTY ORDERED'}</br>
            </td>
            <td width="10%" style="font-size:11;">
                <b>${'QTY SHIPED'}</b>
            </td>
            <td width="10%" style="font-size:11;">
                <b>${'QTY B/O'}</b>
            </td>
            <td width="40%" style="font-size:11;">
                <b>${'PART NO. / DESCRIPTION / VENDOR NO.'}</b>
            </td>
            <td width="15%" style="font-size:11;">
                <b>${'UNIT PRICE'}</b>
            </td>
            <td width="15%" style="font-size:11;">
                <b>${'EXTENDED PRICE'}</b>
            </td>
        </tr>
        </table>
        <table class="basic_table"  style="padding-top:0px; margin-top:0; margin-left:0; text-align:left;" width="100%" height=400px>
        <tr>
            <td style ="border:1px solid black;">
            </td>
        </tr>
        </table>
     %endfor
     
</html>
