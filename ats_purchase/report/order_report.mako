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
        <table class="basic_table1" style="color:white" width="100%">
            <tr>
                <td>
                    <table class="basic_table1" align= 'right' width="45%" height=100px>
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
                                ${'asasfsaf'}
                            </td>
                        </tr>
                    </table>
                </td>
                <td width='10%' style="border-color:white;">
                </td>
                <td>
                    <table class="basic_table1" align= 'right' width="45%" height=100px>
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
                                ${'asasfsaf'}
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
       </table>
     %endfor
</body>
</html>
