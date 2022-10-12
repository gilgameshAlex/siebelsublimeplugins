function sib_tools_send(data) {
    var event = new CustomEvent('sibMessage', {
        detail: data,
        bubbles: true,
        cancelable: true
    });
    document.dispatchEvent(event);
}

$(window).click(function() {
    try {
        var view = SiebelApp.S_App.GetActiveView();
        var _viewName = view.GetName();

        var applet = view.GetActiveApplet();
        var _appletName = applet ? applet.GetName() : "";

        var bc = applet ? applet.GetBusComp() : "";
        var _bcName = bc ? bc.GetName() : "";

        var control = applet ? applet.GetActiveControl() : "";
        var _controlName = control ? control.GetName() : control;

        var _fieldName = control ? control.GetFieldName() : "";
        var _id = bc ? bc.GetFieldValue("Id") : "";

        var _appletContext = [];
        _appletContext.bcName = bc ? bc.GetName() : "";
        var controls = applet ? applet.GetControls() : {};
        controls = Object.values(controls);
        for (var i = 0; i < controls.length; i++) {
            _appletContext.push({
                label: controls[i].GetDisplayName(),
                control: controls[i].GetName(),
                field: controls[i].GetFieldName(),
                value: bc ? bc.GetFieldValue(controls[i].GetFieldName()) : ""
            });
        }

        var _bcContext = [];
        var _bcRec = bc ? bc.GetRecordSet()[bc.GetSelection()] : {};
        _bcRec = _bcRec ? _bcRec : {};
        var fields = Object.keys(_bcRec);
        _bcContext.bcName = bc ? bc.GetName() : "";
        for(var i = 0; i < fields.length; i++){
            _bcContext.push({
                field: fields[i],
                value: _bcRec[fields[i]]
            });
        }

        var message = {
            view: _viewName,
            applet: _appletName,
            bc: _bcName,
            control: _controlName,
            field: _fieldName,
            id: _id,
            appletContext: _appletContext,
            bcContext: _bcContext
        };

        sib_tools_send(message);
    } catch (error) {
        console.log(error);
    }
});

var sibTools = $(`
    <div id="sieb-tools-ext" class="sieb-tools-ext" style="display: none;">
    <div class="select">
        <select name="nav" id="nav">
            <option value="1">Активные объекты</option>
            <option value="2">Ps2json</option>
            <option value="3">Активный апплет</option>
            <option value="4">Активная запись</option>
            <option value="5">GotoView</option>
        </select>
    </div>
    <div id="sieb-tools-hide" style="display: none;"></div>
    <table class="sib-table block block-1">
        <thead>
            <tr class="t-head">
                <td class="bold">Объект</td>
                <td class="bold" style="padding-right: 30px;">Значение</td>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="bold">View:</td>
                <td>
                    <input type="text" class="plain-text autocopy" id="view">
                </td>
            </tr>
            <tr>
                <td class="bold">Applet:</td>
                <td id="">
                    <input type="text" class="plain-text autocopy" id="applet">
                </td>
            </tr>
            <tr>
                <td class="bold">BusComp:</td>
                <td id="">
                    <input type="text" class="plain-text autocopy" id="bc">
                </td>
            </tr>
            <tr>
                <td class="bold">Control:</td>
                <td id="">
                    <input type="text" class="plain-text autocopy" id="control">
                </td>
            </tr>
            <tr>
                <td class="bold">Field:</td>
                <td id="">
                    <input type="text" class="plain-text autocopy" id="field">
                </td>
            </tr>
            <tr>
                <td class="bold">RowId:</td>
                <td id="">
                    <input type="text" class="plain-text autocopy" id="rowId">
                </td>
            </tr>
        </tbody>
    </table>
    <div class="block block-2" style="display: none; padding: 10px;">
        <div><textarea rows="3" id="ps" cols="40"></textarea></div>
        <div style="margin: 10px 0px;"><button id="convert">Convert</button></div>
        <div><textarea id="json" class="autocopy" rows="20" cols="40"></textarea></div>
    </div>
    <div class="block block-3" style="display: none;">
        <div id="appletContext"></div>
    </div>
    <div class="block block-4" style="display: none;">
        <div id="bcContext"></div>
    </div>
    <div class="block block-5" style="display: none;">
        <div style="padding: 10px">
            <input type="text" id="viewName" placeholder="View Name" />
        </div>
        <div style="padding: 10px">
            <input type="text" id="___applet" placeholder="Applet (optional)" />
        </div>
        <div style="padding: 10px">
            <input type="text" id="___rowId" placeholder="Row Id (optional, required when applet is filled)" />
        </div>
        <div style="padding: 10px">
            <button id="gotoView">GotoView</button>
        </div>
    </div>
    </div>
`);

sibTools.click(function(event) {
    event.preventDefault();
    event.stopPropagation();
});

$('body').append(`<style>
        .sieb-tools-ext{
            //opacity: 0.3;
            position: fixed;
            right: 5px; 
            top: 5px;
            border: 2px solid gray;
            border-radius: 6px;
            z-index: 99999999999;
            overflow-y: scroll;
            overflow-x: hidden;
            max-height: 100vh;
        }

        .sieb-tools-ext .select{
            background-color: rgb(60, 60, 60);
            padding: 10px;
        }

        .sieb-tools-ext .select select{
            padding: 2px 6px;
        }

        .sieb-tools-ext #sieb-tools-hide{
            position: absolute;
            top: 6px;
            right: 4px;
            width: 20px;
            height: 20px;
        }

        .block{
            background-color: white;
        }

        .sieb-tools-ext #sieb-tools-hide:after{
            content: "";
            width: 12px;
            height: 20px;
            position: absolute;
            top: -8px;
            left: 4px;
            border-bottom: 2px solid white;
        }

        .sieb-tools-ext.sieb-tools-hidden{
            height: 38px;
            width: 34px;
            background-color: rgb(60, 60, 60);
        }

        .sieb-tools-ext.sieb-tools-hidden .select{
            display: none;
        } 

        .sieb-tools-ext.sieb-tools-hidden table{
            display: none;
        }

        .sieb-tools-ext.sieb-tools-hidden #sieb-tools-hide:before{
            content: "";
            display: block;
            width: 12px;
            height: 12px;
            position: absolute;
            left: 9px;
            top: 5px;
            border-left: 2px solid white;
        }

        .sieb-tools-ext:hover{
            opacity: 1;
        }
        
        .sieb-tools-ext * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: Arial, Helvetica, sans-serif;
        }
        
        .sieb-tools-ext td {
            padding: 5px 15px;
        }

        .sieb-tools-ext .plain-text{
            border: none;
            background-color: transparent;
        }

        .sieb-tools-ext .plain-text:active, .sieb-tools-ext .plain-text:focus{
            box-shadow: none;
            outline: none;
            border: none;
        }
        
        .sieb-tools-ext .bold {
            font-size: 16px;
            font-weight: bold;
        }
        
        .sieb-tools-ext table {
            border-spacing: 0px;
        }
        
        .sieb-tools-ext thead tr{
            background-color: rgb(60, 60, 60);
            color: #ffffff;
        }
        
        .sieb-tools-ext thead td {
            text-align: center;
        }

        .sieb-tools-ext tr{
            background-color: #fff;
        }
        
        .sieb-tools-ext .container {
            border: 2px solid gray;
            border-radius: 6px;
            display: inline-block;
        }
        
        .sieb-tools-ext tbody tr:nth-child(2n+1) {
            background-color: #dedede;
        }
        
        .sieb-tools-ext tbody tr td:first-child {
            text-align: right;
            padding-right: 2px;
        }
        
        .sieb-tools-ext tbody tr td:last-child {
            text-align: left;
            padding-left: 2px;
        }
    </style>`);
$('body').append(sibTools);
$('#sieb-tools-hide').click(function() {
    $('#sieb-tools-ext').toggleClass('sieb-tools-hidden');
})

$('.autocopy').click(function(e) {
    e.target.select();
    document.execCommand('copy');
    $(e.target).trigger('blur');
});

$('select').change(function(e) {
    let val = e.target.value;
    $('.block').css('display', 'none');
    $('.block-' + val).css('display', 'block');
});

ps2json = function(ps) {
    let json = {};
    for (let i = 0; i < ps.GetChildCount(); i++) {
        let childps = ps.GetChild(i);
        let childtype = childps.GetType();
        if (childtype == '') {
            childtype = i;
        }
        if (!json[childtype]) {
            json[childtype] = ps2json(childps);
        } else {
            if (json[childtype].constructor !== Array) {
                json[childtype] = [json[childtype]];
            }
            json[childtype].push(ps2json(childps));
        }
    }
    for (let prop = ps.GetFirstProperty(); prop; prop = ps.GetNextProperty()) {
        json[prop] = ps.GetProperty(prop);
    }
    if (ps.GetValue() != '') {
        json['<Value>'] = ps.GetValue();
    }
    return json;
};

function convert(line) {
    var x = new JSSPropertySet();
    x.DecodeFromString(line);
    var y = ps2json(x);
    return JSON.stringify(y);
}

$('#convert').click(function() {
    let val = $('#ps').val();
    $('#json').val(convert(val));
});

$('#gotoView').click(function(){
    var view = $('#viewName').val();
    var applet = $('#___applet').val();
    var id = $('#___rowId').val();
    var url = window.location.origin + window.location.pathname + '?SWECmd=GotoView&SWEView=' + view.split(' ').join('+');
    url = applet ? (url + '&SWEApplet0=' + applet.split(' ').join('+') + '&SWERowId0=' + id) : url;
    if(view){
        window.SWETargetGotoURL(url);
    }
});