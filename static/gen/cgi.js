function n(t){if(t==0){const r=document.createElementNS("http://www.w3.org/2000/svg","path");return r.setAttribute("d",`M 0.5,0L${.5-Math.sin(Math.PI/3)/2},0.75 ${.5+Math.sin(Math.PI/3)/2},0.75Z`),r.setAttribute("fill","yellow"),r.classList.add("triangle"),r}const e=document.createElementNS("http://www.w3.org/2000/svg","g");e.classList.add("triangle");const a=n(t-1);a.setAttribute("transform","scale(0.5, 0.5) translate(0.5, 0)"),e.appendChild(a);const i=n(t-1);i.setAttribute("transform",`scale(0.5, 0.5) translate(${.5-Math.sin(Math.PI/3)/2}, 0.75)`),e.appendChild(i);const s=n(t-1);return s.setAttribute("transform",`scale(0.5, 0.5) translate(${.5+Math.sin(Math.PI/3)/2}, 0.75)`),e.appendChild(s),e}function l(t){const e=document.getElementById(t.dataset.sierpinskiInput??"sierpinski-input");e!==null?(e.addEventListener("input",a=>{t.querySelectorAll(".triangle").forEach(i=>i.remove()),t.appendChild(n(parseInt(a.target.value)))}),t.appendChild(n(parseInt(e.value)))):t.appendChild(n(1))}document.querySelectorAll("svg.sierpinski").forEach(t=>l(t));