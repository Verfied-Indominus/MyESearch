let departments = {
    'Engineering': [
        'Chemical Engineering',
        'Civil & Environmental Engineering',
        'Mechanical & Manufacturing Engineering',
        'Geomatics Engineering & Land Management',
        'Engineering Institute',
        'Electrical & Computer Engineering',
        'Mechanical and Manufacturing Enterprise Research',
    ],
    'Food & Agriculture': [
        'Agricultural Economics and Extension',
        'Food Production',
        'Publications and Communications Unit',
        'University Farms',
        'Geography'
    ],
    'Humanities & Education': [
        'School of Education',
        'Centre for Language Learning',
        'Creative and Festival Arts',
        'History',
        'Literary, Cultural and Communication Studies',
        'Modern Languages and Linguistics',
        'The Archaeology Centre',
        'The Centre for Language Learning',
        "The Family Development and Children's Research Centre (FDCRC)",
        'The Film Programme'
    ],
    'Law': [
        'Faculty of Law'
    ],
    'Medical Sciences': [
        'Schools of Medicine',
        'Schools of Optometry',
        'Schools of Dentistry',
        'Schools of Nursing',
        'Schools of Pharmacy',
        'Schools of Veterinary Medicine', 
        'Caribbean Centre for Health Systems Research and Development',
        'Centre for Medical Sciences Education',
    ],
    'Science & Technology': [
        'Chemistry',
        'Physics',
        'Life Sciences',
        'Mathematics & Statistics',
        'Computing & Information Technology',
        'Cocoa Research Centre',
        'Seismic Research Unit',
        'The National Herbarium'
    ],
    'Social Sciences': [
        'Behavioural Sciences',
        'Economics',
        'Management Studies',
        'Political Science',
        'Arthur Lok Jack Graduate School for Business',
        'Caribbean Centre for Money and Finance',
        'Centre for Criminology and Criminal Justice',
        'Institute for Gender and Development Studies',
        'Institute of International Relations',
        'Entrepreneurship Unit',
        'Health Economics Unit',
        'Sir Arthur Lewis Institute of Social & Economic Studies',
        'Sustainable Economic Development Unit',
        'Business Development Unit',
    ],
    'Sport': [
        'St. Augustine Academy of Sport'
    ],
}

let faculty = document.getElementById("faculty_select");
let department = document.getElementById("department_select");

faculty.onchange = function() {
    let html = '';

    for (let index in departments[faculty.value]){
        html += `
            <option value="${departments[faculty.value][index]}">${departments[faculty.value][index]}</option>
        `;
    }

    department.innerHTML = html;
}

async function getInterests(){
    let x = 0;
    let researcher_form = document.getElementById("researcher_signup");
    let selected = document.getElementsByClassName('selected');
    let selected_items = [];
    for (let i of selected){
        selected_items[x] = i.innerHTML;
        x += 1;
    };
    selected = await addResearchInterests(selected_items);
    researcher_form.preventDefault;
}



async function addResearchInterests(selected){
    return await fetch(`/interests/${JSON.stringify({'selected': selected})}`);
}




let bar = document.getElementById('js-progressbar');
let img = document.getElementById('img-name');

UIkit.upload('.js-upload', {

    url: '/upload',
    multiple: false,

    beforeSend: function () {
        console.log('beforeSend', arguments);
    },
    beforeAll: function () {
        console.log('beforeAll', arguments);
    },
    load: function () {
        console.log('load', arguments);
    },
    error: function () {
        console.log('error', arguments);
    },
    complete: function () {
        console.log('complete', arguments);
    },

    loadStart: function (e) {
        console.log('loadStart', arguments);

        bar.removeAttribute('hidden');
        bar.max = e.total;
        bar.value = e.loaded;
    },

    progress: function (e) {
        console.log('progress', arguments);

        bar.max = e.total;
        bar.value = e.loaded;
    },

    loadEnd: function (e) {
        console.log('loadEnd', arguments);

        bar.max = e.total;
        bar.value = e.loaded;
    },

    completeAll: function () {
        console.log('completeAll', arguments);

        setTimeout(function () {
            bar.setAttribute('hidden', 'false');
        }, 1000);

        img.innerHTML = `Uploaded ${arguments[0].responseText}`;
    }

});