const ctx = document.getElementById('myChart');

new Chart(ctx, {
    type: 'bar',
    data: {
    labels: ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00'],
    datasets: [{
        label: 'Congestion',
        data: JSON.parse('{{ data }}'),
        borderWidth: 0
    }]
    },
    options: {
    scales: {
        y: {
        beginAtZero: true
        }
    }
    }
});


var myDiv = document.getElementById("myDiv");
var myPet = document.getElementById("myPet");
var ilogo = document.getElementById("ilogo");
var data = myPet.innerHTML;

function checkData() {
    if (data.slice(0,4) == 'Save') {
    myDiv.style.backgroundColor = "#47a6ab";
    myPet.style.color = '#fff'
    ilogo.style.color = '#fff'
    ilogo.classList.add("fa-circle-minus")
    } else if (data.slice(0,5) == 'Extra') {
    myDiv.style.backgroundColor = "#ee4343";
    myPet.style.color = '#fff'
    ilogo.style.color = '#fff'
    ilogo.classList.add("fa-circle-plus")
    } else {
    myDiv.style.backgroundColor = "#fff";
    myPet.style.color = '#00000';
    ilogo.style.color = '#00000'
    ilogo.classList.add("fa-circle-stop")
    }
}
setInterval(checkData, 1);

function init() {
    map = new longdo.Map({
      placeholder: document.getElementById('map')
    });
    map.Route.placeholder(document.getElementById('result'));
    map.Route.add(new longdo.Marker({ lon: parseFloat('{{ og_pos_lon }}'), lat: parseFloat('{{ og_pos_lat }}') },
        { 
            title: '{{ data_temp.og }}', 
            // detail: 'I\'m here' 
        }
    ));
    map.Route.add({ lon: parseFloat('{{ ds_pos_lon }}'), lat: parseFloat('{{ ds_pos_lat }}') });
    map.Route.search();
  }

function checkplan() {
    var plantype = document.getElementById('plantype')
    var dscrp_detail = document.getElementById('dscrp_detail')
    var d_plan = plantype.innerHTML
    if (d_plan.slice(0,4) == 'Safe') {
        dscrp_detail.innerHTML = 'If your appointment is important, this planning time is safe for you to arrive on time.';
        console.log('true');
    }
}