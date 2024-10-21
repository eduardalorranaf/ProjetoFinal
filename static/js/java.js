document.addEventListener('DOMContentLoaded', function() {
    const searchIcon = document.getElementById('toggle-search');
    const searchDropdown = document.getElementById('search-dropdown');
    const userIcon = document.getElementById('user-icon');
    const loginDropdown = document.getElementById('login-dropdown');

    searchIcon.addEventListener('click', function(e) {
        e.preventDefault(); // Previne comportamento padrão do link
        e.stopPropagation();

        if (searchDropdown.classList.contains('active')) {
            searchDropdown.classList.remove('active');
            setTimeout(() => {
                searchDropdown.style.display = 'none';
            }, 300); // Ajusta o tempo para a duração da transição
        } else {
            searchDropdown.style.display = 'block';
            setTimeout(() => {
                searchDropdown.classList.add('active');
            }, 10); // Pequeno delay para permitir transição
            loginDropdown.classList.remove('active');
            loginDropdown.style.display = 'none';
        }
    });

    userIcon.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();

        if (loginDropdown.classList.contains('active')) {
            loginDropdown.classList.remove('active');
            setTimeout(() => {
                loginDropdown.style.display = 'none';
            }, 300);
        } else {
            loginDropdown.style.display = 'block';
            setTimeout(() => {
                loginDropdown.classList.add('active');
            }, 10);
            searchDropdown.classList.remove('active');
            searchDropdown.style.display = 'none';
        }
    });

    document.addEventListener('click', function() {
        searchDropdown.classList.remove('active');
        searchDropdown.style.display = 'none';
        loginDropdown.classList.remove('active');
        loginDropdown.style.display = 'none';
    });

    searchDropdown.addEventListener('click', function(e) {
        e.stopPropagation();
    });

    loginDropdown.addEventListener('click', function(e) {
        e.stopPropagation();
    });
});


const header = document.querySelector('header');

window.addEventListener ('scroll', function(){
    header.classList.toggle ('sticky', this.window.scrollY > 0);
})

let menu = document.querySelector('#menu-icon');
let navmenu = document.querySelector('.navmenu');

menu.onclick = () => {
    menu.classList.toggle('bx-x');
    navmenu.classList.toggle('open');
}

