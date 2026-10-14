
(function(){
  var grid=document.getElementById('listing-grid');
  if(grid){
    var cards=[].slice.call(grid.querySelectorAll('.card'));
    var q=document.getElementById('f-search'),st=document.getElementById('f-status'),
        so=document.getElementById('f-sort'),count=document.getElementById('count-line');
    function apply(){
      var query=(q.value||'').toLowerCase(),status=st.value;
      var vis=cards.filter(function(c){
        var okS=!status||c.dataset.status===status;
        var okQ=!query||c.dataset.search.indexOf(query)>-1;
        return okS&&okQ;});
      var sorted=vis.slice();
      if(so.value==='price-asc')sorted.sort(function(a,b){return (+a.dataset.price||9e15)-(+b.dataset.price||9e15)});
      if(so.value==='price-desc')sorted.sort(function(a,b){return (+b.dataset.price||0)-(+a.dataset.price||0)});
      if(so.value==='beds')sorted.sort(function(a,b){return (+b.dataset.beds||0)-(+a.dataset.beds||0)});
      cards.forEach(function(c){c.style.display='none'});
      sorted.forEach(function(c){c.style.display='';grid.appendChild(c)});
      if(count)count.textContent='Showing '+sorted.length+' of '+cards.length+' homes from the print edition.';
    }
    [q,st,so].forEach(function(el){if(el){el.addEventListener('input',apply);el.addEventListener('change',apply)}});
  }
  var rb=document.getElementById('reveal-btn'),rt=document.getElementById('reveal-target');
  if(rb&&rt){rb.addEventListener('click',function(){rt.hidden=false;rb.hidden=true;var a=rt.querySelector('a');if(a)a.focus();});}
})();
