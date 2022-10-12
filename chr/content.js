var script = document.createElement('script');
script.type = 'text/javascript';
script.src = chrome.extension.getURL("injected.js");
document.body.appendChild(script);

function createTable(obj, id, headers) {
    var table = document.createElement("table");
    table.className = "sib-table";

    var header = document.createElement("thead");
    var tr = document.createElement("tr");
    tr.className = "t-head";
    for(var i = 0; i < headers.length; i++){
        var td = document.createElement("td");
        td.innerText = headers[i];
        tr.appendChild(td);
    }

    header.appendChild(tr);
    table.appendChild(header);

    var tbody = document.createElement('tbody');
    for (var i = 0; i < obj.length; i++) {
        var row = document.createElement("tr");

        var keys = Object.keys(obj[i]);
        for(var j = 0; j < keys.length; j++){         
            var td = document.createElement("td");
            var input = document.createElement("input");
            input.value = obj[i][keys[j]];
            input.className = "plain-text";
            input.addEventListener('click', function(e){
                this.select();
                document.execCommand('copy');
                this.blur();
            });
            td.append(input);
            row.appendChild(td);
        }

        tbody.appendChild(row);
    }

    var context = document.getElementById(id);
    context.innerHTML = "";
    table.appendChild(tbody);
    context.appendChild(table);
}

window.addEventListener("sibMessage", function(event) {
    var data = event.detail;
    document.querySelector('.sieb-tools-ext #view').value = data.view;
    document.querySelector('.sieb-tools-ext #applet').value = data.applet;
    document.querySelector('.sieb-tools-ext #bc').value = data.bc;
    document.querySelector('.sieb-tools-ext #control').value = data.control;
    document.querySelector('.sieb-tools-ext #field').value = data.field;
    document.querySelector('.sieb-tools-ext #rowId').value = data.id;

    createTable(data.appletContext, 'appletContext', ['Заголовок', 'Контрол', 'Поле', 'Значение']);
    createTable(data.bcContext, 'bcContext', ['Поле', 'Значение']);
}, false);