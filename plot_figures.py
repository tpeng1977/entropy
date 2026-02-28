#!/usr/bin/env python3
"""Generate figures for entropy.tex.

Fig 1: Mirror-state paradox — construction + consequence.
Fig 2: P_infty(S;lambda) — translation only vs structural change.
"""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    'text.usetex': True,
    'font.family': 'serif',
    'font.serif': ['Computer Modern Roman'],
    'font.size': 11,
    'axes.labelsize': 13,
    'axes.titlesize': 12,
    'legend.fontsize': 9.5,
    'figure.dpi': 300,
})

BLUE = '#2166ac'
RED  = '#b2182b'


def gauss(x, mu, sigma):
    return np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))


# ═══════════════════════════════════════════════════════════════
# Figure 1 — Mirror-state paradox
# ═══════════════════════════════════════════════════════════════
def fig1_mirror():
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(10.5, 4.0), gridspec_kw={'wspace': 0.30})

    t  = np.linspace(-3, 3, 800)
    i0 = len(t) // 2

    S_A = 2.0 + 0.8 * np.tanh(0.5 * t) + 0.06 * np.sin(3.5 * t)
    S_B = S_A[::-1].copy()
    S0  = S_A[i0]

    # ── panel (a): construction ──
    ax1.plot(t, S_A, color=BLUE, lw=2.3, label=r'$S_A(t)$', zorder=3)
    ax1.plot(t, S_B, color=RED,  lw=2.3, ls='--',
             label=r'$S_B(t)=S_A(2t_0{-}t)$', zorder=3)
    ax1.plot(0, S0, 'ko', ms=7, zorder=5)
    ax1.axvline(0, color='gray', ls=':', lw=0.7, alpha=0.5)

    ax1.text(0.15, S0 - 0.18, r'$t_0$', fontsize=12)

    xr = 1.6
    ir = np.argmin(np.abs(t - xr))
    ax1.annotate(
        r'$\Delta S_A\!\ge\!0$',
        xy=(xr, S_A[ir]), xytext=(2.05, S0 - 0.35),
        fontsize=10, color=BLUE,
        arrowprops=dict(arrowstyle='->', color=BLUE, lw=1.3))
    ax1.annotate(
        r'$\Delta S_B\!\ge\!0$\;?',
        xy=(xr, S_B[ir]), xytext=(2.05, S0 + 0.30),
        fontsize=10, color=RED,
        arrowprops=dict(arrowstyle='->', color=RED, lw=1.3))

    ax1.text(0, S0 + 0.58, r'$S_A(t_0)=S_B(t_0)$',
             ha='center', fontsize=10,
             bbox=dict(boxstyle='round,pad=0.25',
                       fc='white', ec='gray', alpha=0.85))

    ax1.set_xlabel(r'$t$')
    ax1.set_ylabel(r'$S$')
    ax1.set_title(r'\textbf{(a)} Mirror-state construction')
    ax1.legend(loc='lower right', framealpha=0.9)
    ax1.set_xlim(-3, 3.5)
    ax1.set_xticklabels([])
    ax1.set_yticklabels([])

    # ── panel (b): consequence ──
    ax2.plot(t, np.full_like(t, S0), 'k-', lw=2.8, zorder=4,
             label=r'$S(t)=\mathrm{const}$')

    for a, ph in [(0.35, 0), (-0.28, 1.1), (0.22, 2.5)]:
        ax2.plot(t, S0 + a * np.sin(0.9 * t + ph),
                 color='gray', alpha=0.20, lw=1.5)

    for ti in np.linspace(-2, 2, 5):
        ax2.plot(ti, S0, 'ko', ms=4, zorder=5)
        d = 0.25
        ax2.plot([ti - d, ti, ti + d],
                 [S0 + 0.12, S0, S0 + 0.12],
                 color=RED, lw=1.1, zorder=4)

    ax2.text(0, S0 - 0.50,
             r'\textit{Every point is a two-sided local minimum}',
             ha='center', fontsize=10, color='gray')
    ax2.text(0, S0 - 0.66,
             r'$\Rightarrow$ continuous $S(t)$ must be constant.',
             ha='center', fontsize=10, color='gray')

    ax2.set_xlabel(r'$t$')
    ax2.set_ylabel(r'$S$')
    ax2.set_title(r'\textbf{(b)} Consequence of universal monotonicity')
    ax2.legend(loc='upper right', framealpha=0.9)
    ax2.set_xlim(-3, 3)
    ax2.set_ylim(S0 - 0.85, S0 + 0.85)
    ax2.set_xticklabels([])
    ax2.set_yticklabels([])

    fig.savefig('fig_mirror_paradox.pdf', bbox_inches='tight')
    plt.close(fig)
    print('Saved fig_mirror_paradox.pdf')


# ═══════════════════════════════════════════════════════════════
# Figure 2 — P_infty(S;lambda): translation vs structural change
# P_∞ is the long-time distribution of S (no single equilibrium; ongoing fluctuations).
# Traditional view: probability concentrates near maximum entropy (high S).
# ═══════════════════════════════════════════════════════════════
def fig2_distribution():
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(10.5, 4.0), gridspec_kw={'wspace': 0.30})

    S = np.linspace(-1, 9, 800)

    # ── panel (a): translation only ──
    P1 = gauss(S, 4.0, 0.8)
    shift = 1.5
    P2 = gauss(S, 4.0 + shift, 0.8)

    ax1.plot(S, P1, color=BLUE, lw=2.3,
             label=r'$P_\infty^{(E)}(S;\lambda_1)$')
    ax1.fill_between(S, P1, alpha=0.12, color=BLUE)
    ax1.plot(S, P2, color=RED, lw=2.3, ls='--',
             label=r'$P_\infty^{(E)}(S;\lambda_2)$')
    ax1.fill_between(S, P2, alpha=0.12, color=RED)

    pk = gauss(4.0, 4.0, 0.8)
    y_top = max(P1.max(), P2.max()) * 1.35   # headroom so annotation is not clipped
    ax1.set_ylim(0, y_top)
    ax1.annotate('', xy=(4.0 + shift, pk * 1.04),
                 xytext=(4.0, pk * 1.04),
                 arrowprops=dict(arrowstyle='<->', color='gray', lw=1.3))
    ax1.text(4.0 + shift / 2, pk * 1.10, r'$k_B\ln c$',
             ha='center', fontsize=10, color='gray')

    ax1.set_xlabel(r'$S$ (low $\to$ high)')
    ax1.set_ylabel(r'$P_{\infty}^{(E)}(S;\lambda)$')
    ax1.set_title(r'\textbf{(a)} Translation only (common scaling)')
    ax1.legend(framealpha=0.9)
    ax1.set_xticklabels([])
    ax1.set_yticklabels([])

    # ── panel (b): structural change ──
    # Normalized PDFs; no equilibrium — distribution is stochastic. λ_2: bimodal (low-S peak high, high-S peak low).
    S_b = np.linspace(-2, 10, 800)
    S_max = 8.0   # unconstrained: single peak at high S (moved right to avoid overlap)
    S_lo = 1.0   # constraint: low-S peak (taller)
    S_hi = 4.5   # constraint: high-S peak (lower); separated from blue so curves don’t overlap
    sigma_unc = 0.5
    # λ_1 (unconstrained): single narrow peak at S_max
    P1b = gauss(S_b, S_max, sigma_unc)
    # λ_2 (constraint): bimodal, normalized mixture
    w_lo, w_hi = 0.62, 0.38
    P2b = w_lo * gauss(S_b, S_lo, 0.5) + w_hi * gauss(S_b, S_hi, 0.5)

    ax2.plot(S_b, P1b, color=BLUE, lw=2.3,
             label=r'$P_\infty^{(E)}(S;\lambda_1)$')
    ax2.fill_between(S_b, P1b, alpha=0.12, color=BLUE)
    ax2.plot(S_b, P2b, color=RED, lw=2.3, ls='--',
             label=r'$P_\infty^{(E)}(S;\lambda_2)$')
    ax2.fill_between(S_b, P2b, alpha=0.12, color=RED)

    # Headroom: lower apparent curve height so labels fit above
    y2_max = max(P1b.max(), P2b.max()) * 1.4
    ax2.set_ylim(0, y2_max)

    pk_blue = gauss(S_max, S_max, sigma_unc)
    ax2.annotate(r'$S_{\max}$ (unconstrained)',
                 xy=(S_max, pk_blue),
                 xytext=(S_max, pk_blue * 1.22),
                 fontsize=10, color=BLUE, ha='center',
                 arrowprops=dict(arrowstyle='->', color=BLUE, lw=1.2))
    ax2.annotate(r'(high $S$ peak lower)',
                 xy=(S_hi, w_hi * gauss(S_hi, S_hi, 0.5)),
                 xytext=(3.2, w_hi * gauss(S_hi, S_hi, 0.5) * 1.35),
                 fontsize=9, color=RED, style='italic',
                 arrowprops=dict(arrowstyle='->', color=RED, lw=1.0))

    ax2.set_xlabel(r'$S$ (low $\to$ high)')
    ax2.set_ylabel(r'$P_{\infty}^{(E)}(S;\lambda)$')
    ax2.set_title(r'\textbf{(b)} Structural change (constraint-reshaped)')
    ax2.legend(loc='upper left', framealpha=0.9)
    ax2.set_xticklabels([])
    ax2.set_yticklabels([])

    fig.savefig('fig_distribution_change.pdf', bbox_inches='tight')
    plt.close(fig)
    print('Saved fig_distribution_change.pdf')


if __name__ == '__main__':
    fig1_mirror()
    fig2_distribution()
