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
    <% page = 1 %>
     %for o in objects :
            <% setLang(o.partner_id.lang) %>
            <table class="header" style="border-bottom: 0px solid black; width: 100%; ">
            <tr>
                <td style="text-align:right;" width="20%">${ helper.embed_image('png',company.logo,150,90)|n }</td>
                <td style="text-align:left; font-size:11px; width="35%"> <b>   ${company.partner_id.name |entity}</b> </br>
                                                                    %if company and company.partner_id and company.partner_id.street: 
                                                                        ${company.partner_id.street or ''|entity}</br>
                                                                    %endif
                                                                    %if company and company.partner_id and company.partner_id.street2:
                                                                        ${company.partner_id.street2 or ''|entity}</br>
                                                                    %endif
                                                                    %if company and company.partner_id and company.partner_id.city :
                                                                        ${company.partner_id.city or ''|entity}, ${company.partner_id.state_id.code or ''|entity} ${company.partner_id.zip or ''|entity}</br>
                                                                    %endif
                                                                    %if company and company.partner_id and company.partner_id.phone:
                                                                        ${company.partner_id.phone or ''|entity}</br>
                                                                    %endif
                                                                    %if company and company.partner_id and company.partner_id.email:
                                                                        ${company.partner_id.email or ''|entity}</br>
                                                                    %endif
                                                            </td>
                <td style="text-align:center;color:#003366;font-weight:bold; font-size:14px; font-family:UnGungseo;" width="45%">
                        <b>${'Invoice'}</b>
                    <table class="basic_table" style="color:#003366;background-color:#1791d9; " align="right" width="100%">
                                <tr>
                                   <td style="text-align:left;"> 
                                        %if o.number:
                                            <b>${'Invoice No.'} <u>${o.number or ''|entity}</u></b></br>
                                        %else:
                                            <b>${'Invoice No ._______________'}</b></br>
                                        %endif
                                        
                                        %if o.date_invoice:
                                            <b>${'Invoice Date'} <u>${formatLang( o.date_invoice, date=True) or ''|entity}</u></b></br>
                                        %else:
                                            <b>${'Invoice Date_______________'}</b></br>
                                        %endif
                                        
                                        <b>${'Page No.____'} <u>${page or '' | entity}</u>____</br>
                                        %if o.type == 'in_invoice':
                                            <b>${'Purchase Order No.'}   <u> ${o.origin or ''|entity}</u></br>
                                        %else:
                                            <b>${'Purchase Order No._______________'}</b></br>
                                        %endif
                                   </td>                          
                              </tr>
                              
                    </table>
                </td>
            </tr>
            </table>
            <table class="basic_table"  style="display: inline-block; float: left; margin-left:0; text-align:left;" width="45%" height=80px>
                <tr>
                    <td width='1%' style="background-color:#003366; color:white; ">
                        ${'S'}
                        ${'O'}
                        ${'L'}
                        ${'D'}
                        ${""}
                        ${'T'}
                        ${'O'}
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
                        %if o.partner_id and o.partner_id and o.partner_id.shipping_ids:
                            ${o.partner_id and o.partner_id and o.partner_id.shipping_ids[0].name or '' | entity}</br>
                            ${o.partner_id and o.partner_id and o.partner_id.shipping_ids[0].street or ''|entity}</br>
                            %if o.partner_id and o.partner_id and o.partner_id.shipping_ids[0].street2:
                                ${o.partner_id and o.partner_id and o.partner_id.shipping_ids[0].street2 or ''|entity}</br>
                            %endif
                            %if o.partner_id and o.partner_id and o.partner_id.shipping_ids[0].zip:
                                ${o.partner_id and o.partner_id and o.partner_id.shipping_ids[0].zip or ''|entity}
                            %endif
                            %if o.partner_id and o.partner_id and o.partner_id.shipping_ids[0].city:
                                ${o.partner_id and o.partner_id and o.partner_id.shipping_ids[0].city or ''|entity}</br>
                            %endif
                            %if o.partner_id and o.partner_id and o.partner_id.shipping_ids[0].country_id:
                                ${o.partner_id and o.partner_id and o.partner_id.shipping_ids[0].country_id.name or ''|entity}</br>
                            %endif
                           %if o.partner_id and o.partner_id and o.partner_id.shipping_ids[0].phone :
                                ${_("Tel")}: ${o.partner_id and o.partner_id and o.partner_id.shipping_ids[0].phone or ''|entity}</br>
                           %endif
                           %if o.partner_id and o.partner_id and o.partner_id.shipping_ids[0].fax :
                                ${_("Fax")}: ${o.partner_id and o.partner_id and o.partner_id.shipping_ids[0].fax or ''|entity}</br>
                           %endif
                           %if o.partner_id and o.partner_id and o.partner_id.shipping_ids[0].email :
                               ${_("E-mail")}: ${o.partner_id and o.partner_id and o.partner_id.shipping_ids[0].email or ''|entity}</br>
                           %endif
                       %endif
                    </td>
                </tr>
            </table>
            <br/><br/><br/><br/><br/><br/>
            <table class="basic_table" style=" border:1px solid #003366; font-size:14px; margin-left:0;color:#003366;background-color:#1791d9;" width="100%" height=80px>
                <tr>
                    <td width="60%" style="border-style:none;text-align:left;padding-left:30px; ">
                        %if o.type == 'out_invoice':
                            <b>${'SALES ORDER NO.'} ${o.origin or '' |entity}</b>
                        %else:
                            <b>${'SALES ORDER NO.'}</b>
                        %endif
                    </td>
                    <td width="40%" style="border-style:none;text-align:left;">
                        %if o.origin:
                            <b>${'DATE ORDERED: '}${formatLang( sale_date_order(o.id) or '', date=True)|entity}</b>
                        %else:
                            <b>${'DATE ORDERED:'}</b>
                        %endif
                    </td>
                </tr>
                <tr>
                    <td width="60%" style="border-style:none;text-align:left;padding-left:30px; ">
                        <b>${'SALESPERSON:'} ${o.user_id and o.user_id.name or ''|entity}</b>
                    </td>
                    <td width="40%" style="border-style:none;text-align:left;">
                        <b>${'TERMS:'} ${o.payment_term and o.payment_term.name or ''|entity}</b>
                    </td>
                </tr>
                <tr>
                    <td width="60%" style="border-style:none;text-align:left;padding-left:30px; ">
                        <b>${'DATE SHIPPED:'} ${formatLang(ship_date(o.origin,o.id) or '', date=True)|entity}</b>
                    </td>
                    <td width="40%" style="border-style:none;text-align:left;">
                    %if o.origin:
                            <b>${'SHIPPER:'} ${find_shipper(o.origin) or ''|entity}</b>
                        %else:
                            <b>${'SHIPPER:'}</b>
                        %endif
                    </td>
                </tr>
            </table>
            <br/>
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
                    <b>${'PART NO. / DESCRIPTION'}</b>
                </td>
                <td width="15%" style="font-size:11;">
                    <b>${'UNIT PRICE'}</b>
                </td>
                <td width="15%" style="font-size:11;">
                    <b>${'EXTENDED PRICE'}</b>
                </td>
            </tr>
            </table>
            <table class="basic_table" style="table-layout:fixed; margin-top:0; margin-left:0; text-align:left;" width="100%" height=500px>
                <tr>
                    <td style="vertical-align: top;">
                    <table class="basic_table"  style="table-layout:fixed; margin-top:0; margin-left:0; text-align:left;" width="100%">
                        %for line in sale_order_line(o.origin) :
                            <tr>
                                <td width="10%" style ="border-style:none; display: table-cell; vertical-align: top; height="10%">
                                    ${formatLang(line.product_uom_qty ) or '' |entity}
                                </td>
                                <td width="10%" style ="border-style:none; display: table-cell; vertical-align: top; " height="10">
                                    ${shipped_qty(o.id,line)}
                                </td>
                                <td width="10%" style =" border-style:none; display: table-cell; vertical-align: top; " height="10">
                                    ${bo_qty(o.id,line)}
                                </td>
                                <td width="40%" style ="display: table-cell;border-style:none; vertical-align: top; " height="10">
                                    ${line.name or ''|entity}
                                </td>
                                <td width="15%" style ="display: table-cell; vertical-align: top;border-style:none; text-align:right;" height="10">
                                    ${formatLang(line.price_unit, digits=get_digits(dp='Product Price') ) or '' |entity}
                                </td>
                                <td width="15%" style ="display: table-cell;border-style:none; vertical-align: top; text-align:right;" height="10">
                                    ${formatLang(line.price_subtotal, digits=get_digits(dp='Product Price') ) or '' |entity}
                                </td>
                            </tr>
                        %endfor
                    </table>
                    </td>
                 </tr>
            </table>
            <br/>
            <table class="header" style="border-bottom: 0px solid black; width: 100%; ">
                <tr>
                    <td width ="50%" style="text-align:left; color:#003366; font-size:12px; font-weight:bold;"> 
                        </td>
                        <td width ="50%">
                        <table class="basic_table" style="color:#003366; border:1px solid #003366; background-color:#1791d9; font-size:12px; font-weight:bold;" align="right" width="100%">
                                    <tr valign="middle">
                                       <td style="text-align:right; padding-left:2px; border-right:1px solid black;border-bottom:1px solid #1791d9;" width="50%">
                                            ${'SALES AMOUNT'} </br>
                                        </td>
                                        <td width="50%" style="text-align:right;border-bottom:1px solid #1791d9;"> 
                                            ${formatLang(o.amount_untaxed, digits=get_digits(dp='Product Price') ) or '' |entity}
                                        </td>
                                    </tr>
                                    <tr valign="middle">
                                        <td style="text-align:right; padding-left:2px; border-right:1px solid black; border-bottom:1px solid #1791d9;" width="50%">
                                            ${'SHIPPING & HANDLING'}</br>
                                       </td >
                                       <td width="50%" style="border-bottom:1px solid #1791d9;">
                                        </td>
                                  </tr>
                                    <tr valign="middle">
                                        <td style="text-align:right; padding-left:90px; border-right:1px solid black; border-bottom:1px solid black;" width="50%">
                                            ${'SALES TAX'}</br></br>
                                       </td >
                                       <td width="50%" style="border-bottom:1px solid black;">
                                            ${formatLang(o.amount_tax, digits=get_digits(dp='Product Price') ) or '' |entity}
                                        </td>
                                  </tr>
                                  <tr valign="middle">
                                        <td style="text-align:right; padding-left:50px; border-right:1px solid black;" width="50%">
                                            ${'AMOUNT DUE'}</br></br>
                                       </td> 
                                        <td width="50%"> 
                                            ${formatLang(o.residual, digits=get_digits(dp='Product Price') ) or '' |entity}
                                        </td>
                                  </tr>
                        </table>
                    </td>
                </tr>
            </table>
            <table width="100%">
                <tr>
                    <td width="100%" style="font-size:12;">
                        <b>${_('Additional Information:')}</b>
                    </td>
                </tr>
                <tr>
                    <td width="100%" style="font-size:12;">
                        ${o.comment}
                    </td>
                </tr>
            </table>
           <p style="page-break-after:always;">
           </p>
           <% page=page +1 %>
     %endfor
</html>
