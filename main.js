document.documentElement.classList.add('js');
(function(){
  // Mobile-Navigation
  var burger=document.querySelector('.burger'),nav=document.getElementById('nav');
  if(burger&&nav){
    burger.addEventListener('click',function(){
      var o=nav.classList.toggle('open');
      burger.setAttribute('aria-expanded',o);
      document.body.style.overflow=o?'hidden':'';
    });
  }
  // Untermenü per Tastatur/Touch
  document.querySelectorAll('.has-sub>button').forEach(function(b){
    b.addEventListener('click',function(){
      var p=b.parentNode,o=p.classList.toggle('open');b.setAttribute('aria-expanded',o);
    });
  });
  // Reveal on scroll
  var els=document.querySelectorAll('.rv');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(e){e.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{rootMargin:'0px 0px -8% 0px'});
    els.forEach(function(el){io.observe(el)});
  }else els.forEach(function(el){el.classList.add('in')});

  // Öffnungsstatus (Büro)
  var st=document.getElementById('open-now');
  if(st){
    var d=new Date(),day=d.getDay(),m=d.getHours()*60+d.getMinutes(),on=false;
    var spans=day>=1&&day<=4?[[450,720],[780,1020]]:day===5?[[450,720],[780,900]]:[];
    spans.forEach(function(s){if(m>=s[0]&&m<s[1])on=true});
    st.classList.toggle('on',on);
    st.querySelector('b').textContent=on?'Jetzt geöffnet':'Aktuell geschlossen';
  }

  // Nur Lagerware anzeigen
  document.querySelectorAll('[data-stock-toggle]').forEach(function(cb){
    var wrap=document.getElementById(cb.dataset.stockToggle);if(!wrap)return;
    cb.addEventListener('change',function(){
      var rows=wrap.querySelectorAll('tbody tr');
      rows.forEach(function(r){
        if(r.classList.contains('grp'))return;
        var has=r.lastElementChild&&r.lastElementChild.textContent.indexOf('●')>-1;
        r.classList.toggle('is-hidden',cb.checked&&!has);
      });
      rows.forEach(function(r){
        if(!r.classList.contains('grp'))return;
        var n=r.nextElementSibling,any=false;
        while(n&&!n.classList.contains('grp')){if(!n.classList.contains('is-hidden'))any=true;n=n.nextElementSibling}
        r.classList.toggle('is-hidden',cb.checked&&!any);
      });
    });
  });

  // Abschnitt per Chip/Link öffnen
  function openHash(){var h=location.hash.slice(1),el=h&&document.getElementById(h);if(el&&el.tagName==='DETAILS')el.open=true}
  window.addEventListener('hashchange',openHash);openHash();
  document.querySelectorAll('.chip[href^="#"]').forEach(function(c){c.addEventListener('click',function(){var el=document.getElementById(c.getAttribute('href').slice(1));if(el&&el.tagName==='DETAILS')el.open=true})});

  // Chipbar: aktiven Abschnitt markieren
  var chips=document.querySelectorAll('.chip[href^="#"]');
  if(chips.length&&'IntersectionObserver' in window){
    var map={};chips.forEach(function(c){map[c.getAttribute('href').slice(1)]=c});
    var so=new IntersectionObserver(function(es){es.forEach(function(e){
      if(e.isIntersecting){chips.forEach(function(c){c.classList.remove('on')});var c=map[e.target.id];if(c){c.classList.add('on');var bar=c.parentNode;bar.scrollLeft=c.offsetLeft-bar.clientWidth/2+c.offsetWidth/2}}
    })},{rootMargin:'-160px 0px -65% 0px'});
    Object.keys(map).forEach(function(id){var el=document.getElementById(id);if(el)so.observe(el)});
  }

  // Kontaktformular -> E-Mail-Programm (bis ein Formular-Backend angebunden ist)
  var f=document.getElementById('kontaktform');
  if(f){
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var g=function(n){return (f.elements[n]&&f.elements[n].value||'').trim()};
      var body='Anrede: '+g('anrede')+'\nName: '+g('vorname')+' '+g('nachname')+'\nE-Mail: '+g('email')+'\nTelefon: '+g('telefon')+'\n\n'+g('nachricht');
      location.href='mailto:info@mueller-welte.de?subject='+encodeURIComponent(g('betreff'))+'&body='+encodeURIComponent(body);
    });
  }
})();
