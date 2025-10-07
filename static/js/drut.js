document.addEventListener("DOMContentLoaded", function() {
  const ilosc = document.getElementById("ilosc");
  const waga = document.getElementById("waga");
  const suma = document.getElementById("suma");

  function przeliczSume() {
    const il = parseFloat(ilosc.value) || 0;
    const wg = parseFloat(waga.value) || 0;
    suma.value = (il * wg).toFixed(2);
  }

  ilosc.addEventListener("input", przeliczSume);
  waga.addEventListener("input", przeliczSume);
});

const role = "{{ role }}";  // pamiętaj, żeby w HTML wstawić wartość roli admina

// debounce helper
function debounce(fn, delay) {
  let t;
  return function(...args) {
    clearTimeout(t);
    t = setTimeout(() => fn.apply(this, args), delay);
  }
}

async function fetchDrut(q) {
  const url = '/drut/search?q=' + encodeURIComponent(q);
  const res = await fetch(url);
  if (!res.ok) return;
  const body = document.getElementById('drutBody');
  body.innerHTML = '';
  const data = await res.json();

  data.forEach(row => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${row.stan||''}</td>
      <td>${row.srednica_drutu||''}</td>
      <td>${row.gatunek_drutu||''}</td>
      <td>${row.dostawca||''}</td>
      <td>${row.ilosc_szpule_kregi||''}</td>
      <td>${row.rodzaj||''}</td>
      <td>${row.waga||''}</td>
      <td>${row.suma_kg||''}</td>
      <td>${row.partia_materialu_nr||''}</td>
      <td>${row.przewidywana_data_dostawy||''}</td>
      <td>${row.przyjecie_materialu||''}</td>
      ${role === 'admin' ? `
      <td>
        <button class="btn btn-sm btn-primary" data-bs-toggle="modal" data-bs-target="#editModal${row.id}">Edytuj</button>
        <form method="post" action="/drut/delete/${row.id}" style="display:inline;">
          <button class="btn btn-sm btn-danger" onclick="return confirm('Usuń rekord?')">Usuń</button>
        </form>
      </td>` : ''}
    `;
    body.appendChild(tr);
  });
}

const inputD = document.getElementById('searchDrut');
inputD.addEventListener('keyup', debounce((e) => {
  fetchDrut(e.target.value);
}, 250));
