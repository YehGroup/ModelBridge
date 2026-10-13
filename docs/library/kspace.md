# Real-space and reciprocal-lattice transformation

For the triangular Bravais lattice of MoS$_2$, let

$$
\mathbf a_1=a\begin{pmatrix}1\\0\end{pmatrix},\qquad
\mathbf a_2=a\begin{pmatrix}-\frac12\\\frac{\sqrt3}{2}\end{pmatrix},\qquad
A=(\mathbf a_1\ \mathbf a_2)=a\begin{pmatrix}1&-\frac12\\0&\frac{\sqrt3}{2}\end{pmatrix}.
$$

The reciprocal basis is defined by $\mathbf a_i\cdot\mathbf b_j=2\pi\delta_{ij}$. Consequently, $A^{\mathsf T}B=2\pi I$, so

$$
B=2\pi(A^{-1})^{\mathsf T}=\frac{2\pi}{a}\begin{pmatrix}1&0\\\frac1{\sqrt3}&\frac2{\sqrt3}\end{pmatrix},\qquad
\mathbf b_1=\frac{2\pi}{a}\begin{pmatrix}1\\1/\sqrt3\end{pmatrix},\qquad
\mathbf b_2=\frac{2\pi}{a}\begin{pmatrix}0\\2/\sqrt3\end{pmatrix}.
$$

The unique linear mapping from real-space to the reciprocal-space is

$$
T=BA^{-1}=\frac{2\pi}{a^2}\begin{pmatrix}1&1/\sqrt3\\1/\sqrt3&5/3\end{pmatrix},\qquad
T(n\mathbf a_1+m\mathbf a_2)=n\mathbf b_1+m\mathbf b_2.
$$

The right-hand plot uses normalized reciprocal coordinates $\widetilde{\mathbf k}=\mathbf k/(2\pi/a)$; both plots set $a=1$.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 330" width="100%" role="img" aria-label="Real-space triangular lattice and its linearly transformed reciprocal-space image; 13 atoms and 15 bonds each">
<defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" fill="#e88800"/></marker></defs>
<text x="215" y="20" text-anchor="middle" font-size="18" font-weight="600" fill="currentColor">Real space</text>
<text x="635" y="20" text-anchor="middle" font-size="18" font-weight="600" fill="currentColor">Reciprocal space</text>
<g id="real">
<line x1="210.00" y1="174.00" x2="162.00" y2="146.29" stroke="currentColor" stroke-width="1.8"/>
<line x1="210.00" y1="174.00" x2="258.00" y2="146.29" stroke="currentColor" stroke-width="1.8"/>
<line x1="210.00" y1="174.00" x2="210.00" y2="229.43" stroke="currentColor" stroke-width="1.8"/>
<line x1="162.00" y1="90.86" x2="210.00" y2="63.15" stroke="currentColor" stroke-width="1.8"/>
<line x1="258.00" y1="90.86" x2="210.00" y2="63.15" stroke="currentColor" stroke-width="1.8"/>
<line x1="162.00" y1="90.86" x2="162.00" y2="146.29" stroke="currentColor" stroke-width="1.8"/>
<line x1="258.00" y1="90.86" x2="258.00" y2="146.29" stroke="currentColor" stroke-width="1.8"/>
<line x1="114.00" y1="174.00" x2="162.00" y2="146.29" stroke="currentColor" stroke-width="1.8"/>
<line x1="114.00" y1="174.00" x2="114.00" y2="229.43" stroke="currentColor" stroke-width="1.8"/>
<line x1="306.00" y1="174.00" x2="258.00" y2="146.29" stroke="currentColor" stroke-width="1.8"/>
<line x1="306.00" y1="174.00" x2="306.00" y2="229.43" stroke="currentColor" stroke-width="1.8"/>
<line x1="162.00" y1="257.14" x2="114.00" y2="229.43" stroke="currentColor" stroke-width="1.8"/>
<line x1="162.00" y1="257.14" x2="210.00" y2="229.43" stroke="currentColor" stroke-width="1.8"/>
<line x1="258.00" y1="257.14" x2="210.00" y2="229.43" stroke="currentColor" stroke-width="1.8"/>
<line x1="258.00" y1="257.14" x2="306.00" y2="229.43" stroke="currentColor" stroke-width="1.8"/>
<circle cx="210.00" cy="174.00" r="6.2" fill="#1957ea"/>
<circle cx="114.00" cy="174.00" r="6.2" fill="#1957ea"/>
<circle cx="306.00" cy="174.00" r="6.2" fill="#1957ea"/>
<circle cx="162.00" cy="90.86" r="6.2" fill="#1957ea"/>
<circle cx="258.00" cy="90.86" r="6.2" fill="#1957ea"/>
<circle cx="162.00" cy="257.14" r="6.2" fill="#1957ea"/>
<circle cx="258.00" cy="257.14" r="6.2" fill="#1957ea"/>
<circle cx="210.00" cy="63.15" r="6.2" fill="#059822"/>
<circle cx="162.00" cy="146.29" r="6.2" fill="#059822"/>
<circle cx="258.00" cy="146.29" r="6.2" fill="#059822"/>
<circle cx="114.00" cy="229.43" r="6.2" fill="#059822"/>
<circle cx="210.00" cy="229.43" r="6.2" fill="#059822"/>
<circle cx="306.00" cy="229.43" r="6.2" fill="#059822"/>
<line x1="210.00" y1="174.00" x2="306.00" y2="174.00" stroke="#e88800" stroke-width="2.5" marker-end="url(#arr)"/>
<text x="248.00" y="192.00" font-size="16" fill="#d77d00">a<tspan baseline-shift="sub" font-size="11">1</tspan></text>
<line x1="210.00" y1="174.00" x2="162.00" y2="90.86" stroke="#e88800" stroke-width="2.5" marker-end="url(#arr)"/>
<text x="190.00" y="130.43" font-size="16" fill="#d77d00">a<tspan baseline-shift="sub" font-size="11">2</tspan></text>
</g>
<g id="reciprocal">
<line x1="634.00" y1="183.00" x2="608.00" y2="167.99" stroke="currentColor" stroke-width="1.8"/>
<line x1="634.00" y1="183.00" x2="686.00" y2="122.96" stroke="currentColor" stroke-width="1.8"/>
<line x1="634.00" y1="183.00" x2="608.00" y2="258.06" stroke="currentColor" stroke-width="1.8"/>
<line x1="634.00" y1="92.93" x2="686.00" y2="32.89" stroke="currentColor" stroke-width="1.8"/>
<line x1="712.00" y1="47.90" x2="686.00" y2="32.89" stroke="currentColor" stroke-width="1.8"/>
<line x1="634.00" y1="92.93" x2="608.00" y2="167.99" stroke="currentColor" stroke-width="1.8"/>
<line x1="712.00" y1="47.90" x2="686.00" y2="122.96" stroke="currentColor" stroke-width="1.8"/>
<line x1="556.00" y1="228.03" x2="608.00" y2="167.99" stroke="currentColor" stroke-width="1.8"/>
<line x1="556.00" y1="228.03" x2="530.00" y2="303.09" stroke="currentColor" stroke-width="1.8"/>
<line x1="712.00" y1="137.97" x2="686.00" y2="122.96" stroke="currentColor" stroke-width="1.8"/>
<line x1="712.00" y1="137.97" x2="686.00" y2="213.02" stroke="currentColor" stroke-width="1.8"/>
<line x1="556.00" y1="318.10" x2="530.00" y2="303.09" stroke="currentColor" stroke-width="1.8"/>
<line x1="556.00" y1="318.10" x2="608.00" y2="258.06" stroke="currentColor" stroke-width="1.8"/>
<line x1="634.00" y1="273.07" x2="608.00" y2="258.06" stroke="currentColor" stroke-width="1.8"/>
<line x1="634.00" y1="273.07" x2="686.00" y2="213.02" stroke="currentColor" stroke-width="1.8"/>
<circle cx="634.00" cy="183.00" r="6.2" fill="#1957ea"/>
<circle cx="556.00" cy="228.03" r="6.2" fill="#1957ea"/>
<circle cx="712.00" cy="137.97" r="6.2" fill="#1957ea"/>
<circle cx="634.00" cy="92.93" r="6.2" fill="#1957ea"/>
<circle cx="712.00" cy="47.90" r="6.2" fill="#1957ea"/>
<circle cx="556.00" cy="318.10" r="6.2" fill="#1957ea"/>
<circle cx="634.00" cy="273.07" r="6.2" fill="#1957ea"/>
<circle cx="686.00" cy="32.89" r="6.2" fill="#059822"/>
<circle cx="608.00" cy="167.99" r="6.2" fill="#059822"/>
<circle cx="686.00" cy="122.96" r="6.2" fill="#059822"/>
<circle cx="530.00" cy="303.09" r="6.2" fill="#059822"/>
<circle cx="608.00" cy="258.06" r="6.2" fill="#059822"/>
<circle cx="686.00" cy="213.02" r="6.2" fill="#059822"/>
<line x1="634.00" y1="183.00" x2="712.00" y2="137.97" stroke="#e88800" stroke-width="2.5" marker-end="url(#arr)"/>
<text x="663.00" y="178.48" font-size="16" fill="#d77d00">b<tspan baseline-shift="sub" font-size="11">1</tspan></text>
<line x1="634.00" y1="183.00" x2="634.00" y2="92.93" stroke="#e88800" stroke-width="2.5" marker-end="url(#arr)"/>
<text x="640.00" y="135.97" font-size="16" fill="#d77d00">b<tspan baseline-shift="sub" font-size="11">2</tspan></text>
</g>
</svg>
