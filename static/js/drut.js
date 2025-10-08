document.addEventListener("DOMContentLoaded", function() {
  const role = "{{ role }}"; // wstawiana rola admina z HTML

  // --- Przeliczanie suma = ilość x waga w formularzu dodawania ---
  const ilosc = document.getElementById("ilosc");
  const waga = document.getElementById("waga");
  const suma = document.getElementById("suma");

  function przeliczSume(elI, elW, elS) {
    const il = parseFloat(elI.value) || 0;
    const wg = parseFloat(elW.value) || 0;
    elS.value = (il * wg).toFixed(2);
  }

  if (ilosc && waga && suma) {
    ilosc.addEventListener("input", () => przeliczSume(ilosc, waga, suma));
    waga.addEventListener("input", () => przeliczSume(ilosc, waga, suma));
  }

  // --- Przeliczanie i ustawianie select w modalach edycji ---
  const modals = document.querySelectorAll('.modal');
  modals.forEach(modal => {
    modal.addEventListener('shown.bs.modal', function () {
      const id = modal.id.split('editModal')[1];
      const il = document.getElementById('ilosc-' + id);
      const wg = document.getElementById('waga-' + id);
      const sm = document.getElementById('suma-' + id);
      const selectRodzaj = modal.querySelector('select[name="rodzaj"]');

      if (!il || !wg || !sm || !selectRodzaj) return;

      // Przelicz od razu po otwarciu modala
      przeliczSume(il, wg, sm);

      // Ustaw aktualną wartość select z data-rodzaj
      const aktualna = il.dataset.rodzaj || '';
      if (aktualna) {
        selectRodzaj.value = aktualna;
      }

      // Podpinamy event listener na zmianę pól
      const handler = () => przeliczSume(il, wg, sm);
      il.addEventListener('input', handler);
      wg.addEventListener('input', handler);
    });
  });

  // --- Live search filtrujący istniejące wiersze ---
  const searchInput = document.getElementById('searchDrut');
  searchInput.addEventListener('input', function() {
    const filter = this.value.toLowerCase();
    const rows = document.querySelectorAll('#drutBody tr');

    rows.forEach(row => {
      let match = false;
      row.querySelectorAll('td').forEach(cell => {
        if (cell.textContent.toLowerCase().includes(filter)) {
          match = true;
        }
      });
      row.style.display = match ? '' : 'none';
    });
  });
});
