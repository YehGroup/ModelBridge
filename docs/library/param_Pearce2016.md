# Parameters (`to be determined`)


## Change of basis

In [Fang et al. (2018)](references.md#fang2018), their basis $\mathcal{B}_F$ that is different from the basis $\mathcal{B}_P$ in [Pearce et all. (2016)](references.md#pearce2016). As shown below

$$
\mathcal{B}_F = 
\left\{
\underbrace{d_{xz}^{o},d_{yz}^{o}}_{A},
\ 
\underbrace{p_x^{o},p_y^{o},p_z^{o}}_{B},
\ 
\underbrace{d_{xy}^{e},d_{x^2-y^2}^{e},d_{z^2}^{e}}_{C},
\ 
\underbrace{p_x^{e},p_y^{e},p_z^{e}}_{D}
\right\}
$$

This incentivise us to define the Pearce basis in exactly the corresponding block order

$$
\mathcal{B}_P =
\left\{
\underbrace{d_1,d_{-1}}_{A},
\ 
\underbrace{p_1^{A},p_{-1}^{A},p_z^{S}}_{B},
\ 
\underbrace{d_2,d_{-2},d_{z^2}}_{C},
\ 
\underbrace{p_1^{S},p_{-1}^{S},p_z^{A}}_{D}
\right\}
$$

The conversion is

$$
\begin{align}
    d_{\pm 1} &= \frac{1}{\sqrt{2}} \left(d_{xz}^o \pm i d_{yz}^o\right)\\
    p_{\pm 1}^A &= \frac{1}{\sqrt{2}} \left(p_{x}^o \pm i p_{y}^o\right)\\
    p_{z}^S &= p_{z}^o\\
    d_{\pm 2} &= \frac{1}{\sqrt{2}} \left(d_{x^2-y^2}^e \pm i d_{xy}^e\right)\\
    d_{z^2} &= d_{z^2}^e\\
    p_{\pm 1}^S &= \frac{1}{\sqrt{2}} \left(p_{x}^e \pm i p_{y}^e\right)\\
    p_{z}^A &= p_{z}^e\\
\end{align}
$$

which gives rise to the change of basis

$$
U = \begin{bmatrix} 
              U_A & [0] & [0] & [0] \\ 
              [0] & U_B & [0] & [0] \\ 
              [0] & [0] & U_C & [0] \\ 
              [0] & [0] & [0] & U_D \\ 
          \end{bmatrix}
$$

<figure markdown="block">

$$
U_A = \frac{1}{\sqrt{2}}
        \begin{bmatrix} 
            1 & 1 \\
            i & -i \\ 
        \end{bmatrix}
\quad,\quad
U_B = \begin{bmatrix} 
        \frac{1}{\sqrt{2}} \begin{pmatrix}
            1 & 1 \\
            i & -i \\
        \end{pmatrix} & \begin{matrix} 0 \\ 0 \end{matrix} \\
        \begin{matrix} 0 & \ \ \ 0 \end{matrix} & 1
    \end{bmatrix}
\quad,\quad
U_C = \begin{bmatrix} 
        \frac{1}{\sqrt{2}} \begin{pmatrix}
            i & -i \\
            1 & 1 \\
        \end{pmatrix} & \begin{matrix} 0 \\ 0 \end{matrix} \\
        \begin{matrix} 0 & \ \ \ 0 \end{matrix} & 1
    \end{bmatrix}
\quad,\quad
U_D = \begin{bmatrix} 
        \frac{1}{\sqrt{2}} \begin{pmatrix}
            1 & 1 \\
            i & -i \\
        \end{pmatrix} & \begin{matrix} 0 \\ 0 \end{matrix} \\
        \begin{matrix} 0 & \ \ \ 0 \end{matrix} & 1
    \end{bmatrix}
$$

Then $UHU^\dagger$ will give the constructed Hamiltonian from [Pearce et all. (2016)](references.md#pearce2016) in basis of [Fang et al. (2018)](references.md#fang2018).

