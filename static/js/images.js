function teamOne() {
    let team1 = document.getElementById('team1')
    let team1Image = document.querySelector('.predict__team1-logo')
    team1Image.setAttribute('src', '../static/imgs/logos/' + team1.options[team1.selectedIndex].value + '.png')
    team1Image.setAttribute('alt', team1.options[team1.selectedIndex].value)
    team1Image.setAttribute('title', team1.options[team1.selectedIndex].value)

}

function teamTwo() {
    let team2 = document.getElementById('team2')
    let team2Image = document.querySelector('.predict__team2-logo')
    team2Image.setAttribute('src', '../static/imgs/logos/' + team2.options[team2.selectedIndex].value + '.png')
    team2Image.setAttribute('alt', team2.options[team2.selectedIndex].value)
    team2Image.setAttribute('title', team2.options[team2.selectedIndex].value)

}

function map_logo() {
    let map_name = document.getElementById('map');
    let mapImage = document.querySelector('#predict__map-logo');
    mapImage.setAttribute('src', '../static/imgs/map_logos/' + map_name.options[map_name.selectedIndex].value + '.png')
    mapImage.setAttribute('alt', map_name.options[map_name.selectedIndex].value)
    mapImage.setAttribute('title', map_name.options[map_name.selectedIndex].value)
}

$('#predict__form').submit(function () {
    let team1 = document.getElementById('team1');
    // let team1 = '5POWER';
    // let team2 = '1WIN';
    let team2 = document.getElementById('team2')


    if (team1.options[team1.selectedIndex].value !== team2.options[team2.selectedIndex].value)
        return true;
    else {
        document.querySelector('.banner').classList.toggle('on');
        document.querySelector('.banner').classList.toggle('off');

        return false;
    }
});

let button = document.querySelector('.banner__button');
button.onclick = function () {
    document.querySelector('.banner').classList.toggle('on');
    document.querySelector('.banner').classList.toggle('off');
}
