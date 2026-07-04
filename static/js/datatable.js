/* Doctoralis — enhance every <table class="data"> with search, sort, CSV & print.
   Zero dependencies, auto-runs on load. */
(function () {
  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  var SEARCH_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>';
  var CSV_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>';
  var PRINT_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9V2h12v7M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2M6 14h12v8H6z"/></svg>';

  function rowText(tr) {
    return (tr.innerText || tr.textContent || '').replace(/\s+/g, ' ').trim().toLowerCase();
  }
  function isDataRow(tr) {
    // skip the "empty state" row that spans all columns
    return !tr.querySelector('td[colspan]');
  }
  function cellText(tr, i) {
    var c = tr.cells[i];
    return c ? (c.innerText || c.textContent || '').trim() : '';
  }
  function looksNumeric(s) { return /^-?[\d\s.,]+$/.test(s) && /\d/.test(s); }
  function toNum(s) { return parseFloat(s.replace(/\s/g, '').replace(',', '.')); }

  function enhance(table) {
    if (table.dataset.dtReady) return;
    var tbody = table.tBodies[0];
    if (!tbody) return;
    var allRows = Array.prototype.slice.call(tbody.rows);
    var dataRows = allRows.filter(isDataRow);
    if (dataRows.length === 0) return;           // nothing to enhance
    table.dataset.dtReady = '1';

    var wrap = table.closest('.table-wrap') || table.parentElement;

    // ---- toolbar ----
    var bar = document.createElement('div');
    bar.className = 'dt-toolbar';
    bar.innerHTML =
      '<div class="dt-search">' + SEARCH_ICON +
      '<input type="search" placeholder="Rechercher…" aria-label="Rechercher"></div>' +
      '<div class="dt-actions">' +
      '<span class="dt-count"></span>' +
      '<button type="button" class="dt-btn" data-act="csv">' + CSV_ICON + 'Exporter CSV</button>' +
      '<button type="button" class="dt-btn" data-act="print">' + PRINT_ICON + 'Imprimer</button>' +
      '</div>';
    wrap.parentNode.insertBefore(bar, wrap);

    var input = bar.querySelector('input');
    var countEl = bar.querySelector('.dt-count');

    function updateCount() {
      var visible = dataRows.filter(function (r) { return r.style.display !== 'none'; }).length;
      countEl.textContent = visible + ' / ' + dataRows.length + ' résultat' + (dataRows.length > 1 ? 's' : '');
    }
    updateCount();

    // ---- search ----
    input.addEventListener('input', function () {
      var q = input.value.trim().toLowerCase();
      dataRows.forEach(function (r) {
        r.style.display = (!q || rowText(r).indexOf(q) > -1) ? '' : 'none';
      });
      updateCount();
    });

    // ---- sort ----
    var ths = table.tHead ? table.tHead.rows[0].cells : [];
    Array.prototype.forEach.call(ths, function (th, i) {
      th.classList.add('dt-th');
      th.addEventListener('click', function () {
        var asc = th.classList.contains('dt-asc') ? false : true;
        Array.prototype.forEach.call(ths, function (t) { t.classList.remove('dt-asc', 'dt-desc'); });
        th.classList.add(asc ? 'dt-asc' : 'dt-desc');
        var sorted = dataRows.slice().sort(function (a, b) {
          var x = cellText(a, i), y = cellText(b, i);
          var r;
          if (looksNumeric(x) && looksNumeric(y)) r = toNum(x) - toNum(y);
          else r = x.localeCompare(y, 'fr', { numeric: true });
          return asc ? r : -r;
        });
        sorted.forEach(function (r) { tbody.appendChild(r); });
      });
    });

    // ---- actions ----
    bar.querySelector('[data-act=csv]').addEventListener('click', function () { exportCSV(table, dataRows); });
    bar.querySelector('[data-act=print]').addEventListener('click', function () { window.print(); });
  }

  function csvCell(t) {
    t = (t || '').replace(/\s+/g, ' ').trim();
    return '"' + t.replace(/"/g, '""') + '"';
  }
  function exportCSV(table, dataRows) {
    var lines = [];
    if (table.tHead) {
      lines.push(Array.prototype.map.call(table.tHead.rows[0].cells, function (c) {
        return csvCell(c.innerText || c.textContent);
      }).join(','));
    }
    dataRows.forEach(function (r) {
      if (r.style.display === 'none') return;
      lines.push(Array.prototype.map.call(r.cells, function (c) {
        return csvCell(c.innerText || c.textContent);
      }).join(','));
    });
    var content = '﻿' + lines.join('\r\n');   // BOM for Excel/accents
    var a = document.createElement('a');
    a.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(content);
    a.download = 'doctoralis-export-' + new Date().toISOString().slice(0, 10) + '.csv';
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
  }

  ready(function () {
    Array.prototype.forEach.call(document.querySelectorAll('table.data'), enhance);
  });
})();
