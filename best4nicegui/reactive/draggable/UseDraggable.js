const N = Vue.unref
const T = Vue.isRef
const W = Vue.toRefs
const X = Vue.customRef
const Y = Vue.getCurrentScope
const H = Vue.onScopeDispose
const h = Vue.ref
const x = Vue.computed
const S = Vue.watch
const U = Vue.defineComponent
const q = Vue.onMounted
function z(e) {
  return Y() ? (H(e), !0) : !1;
}
function u(e) {
  return typeof e == "function" ? e() : N(e);
}
const I = typeof window < "u", F = () => {
};
var G = Object.defineProperty, J = Object.defineProperties, K = Object.getOwnPropertyDescriptors, E = Object.getOwnPropertySymbols, Q = Object.prototype.hasOwnProperty, Z = Object.prototype.propertyIsEnumerable, D = (e, r, t) => r in e ? G(e, r, { enumerable: !0, configurable: !0, writable: !0, value: t }) : e[r] = t, j = (e, r) => {
  for (var t in r || (r = {}))
    Q.call(r, t) && D(e, t, r[t]);
  if (E)
    for (var t of E(r))
      Z.call(r, t) && D(e, t, r[t]);
  return e;
}, k = (e, r) => J(e, K(r));
function R(e) {
  if (!T(e))
    return W(e);
  const r = Array.isArray(e.value) ? new Array(e.value.length) : {};
  for (const t in e.value)
    r[t] = X(() => ({
      get() {
        return e.value[t];
      },
      set(o) {
        if (Array.isArray(e.value)) {
          const a = [...e.value];
          a[t] = o, e.value = a;
        } else {
          const a = k(j({}, e.value), { [t]: o });
          Object.setPrototypeOf(a, e.value), e.value = a;
        }
      }
    }));
  return r;
}
function ee(e) {
  var r;
  const t = u(e);
  return (r = t == null ? void 0 : t.$el) != null ? r : t;
}
const V = I ? window : void 0;
function $(...e) {
  let r, t, o, a;
  if (typeof e[0] == "string" || Array.isArray(e[0]) ? ([t, o, a] = e, r = V) : [r, t, o, a] = e, !r)
    return F;
  Array.isArray(t) || (t = [t]), Array.isArray(o) || (o = [o]);
  const p = [], d = () => {
    p.forEach((i) => i()), p.length = 0;
  }, g = (i, _, s, f) => (i.addEventListener(_, s, f), () => i.removeEventListener(_, s, f)), y = S(
    () => [ee(r), u(a)],
    ([i, _]) => {
      d(), i && p.push(
        ...t.flatMap((s) => o.map((f) => g(i, s, f, _)))
      );
    },
    { immediate: !0, flush: "post" }
  ), c = () => {
    y(), d();
  };
  return z(c), c;
}
var re = Object.defineProperty, te = Object.defineProperties, ne = Object.getOwnPropertyDescriptors, A = Object.getOwnPropertySymbols, oe = Object.prototype.hasOwnProperty, ae = Object.prototype.propertyIsEnumerable, b = (e, r, t) => r in e ? re(e, r, { enumerable: !0, configurable: !0, writable: !0, value: t }) : e[r] = t, ie = (e, r) => {
  for (var t in r || (r = {}))
    oe.call(r, t) && b(e, t, r[t]);
  if (A)
    for (var t of A(r))
      ae.call(r, t) && b(e, t, r[t]);
  return e;
}, se = (e, r) => te(e, ne(r));
function le(e, r = {}) {
  var t, o;
  const {
    pointerTypes: a,
    preventDefault: p,
    stopPropagation: d,
    exact: g,
    onMove: y,
    onEnd: c,
    onStart: i,
    initialValue: _,
    axis: s = "both",
    draggingElement: f = V,
    handle: C = e
  } = r, l = h(
    (t = u(_)) != null ? t : { x: 0, y: 0 }
  ), v = h(), P = (n) => a ? a.includes(n.pointerType) : !0, w = (n) => {
    u(p) && n.preventDefault(), u(d) && n.stopPropagation();
  }, L = (n) => {
    if (!P(n) || u(g) && n.target !== u(e))
      return;
    const m = u(e).getBoundingClientRect(), O = {
      x: n.clientX - m.left,
      y: n.clientY - m.top
    };
    (i == null ? void 0 : i(O, n)) !== !1 && (v.value = O, w(n));
  }, M = (n) => {
    if (!P(n) || !v.value)
      return;
    let { x: m, y: O } = l.value;
    (s === "x" || s === "both") && (m = n.clientX - v.value.x), (s === "y" || s === "both") && (O = n.clientY - v.value.y), l.value = {
      x: m,
      y: O
    }, y == null || y(l.value, n), w(n);
  }, B = (n) => {
    P(n) && v.value && (v.value = void 0, c == null || c(l.value, n), w(n));
  };
  if (I) {
    const n = { capture: (o = r.capture) != null ? o : !0 };
    $(C, "pointerdown", L, n), $(f, "pointermove", M, n), $(f, "pointerup", B, n);
  }
  return se(ie({}, R(l)), {
    position: l,
    isDragging: x(() => !!v.value),
    style: x(
      () => `left:${l.value.x}px;top:${l.value.y}px;`
    )
  });
}
const pe = /* @__PURE__ */ U({
  __name: "UseDraggable",
  props: {
    elementId: null
  },
  emits: ["update"],
  setup(e, { emit: r }) {
    const t = e;
    return q(() => {
      const o = document.getElementById(t.elementId), { x: a, y: p, style: d } = le(o, {
        initialValue: { x: 400, y: 400 }
      });
      S([a, p, d], ([g, y, c]) => {
        r("update", { x: g, y, style: c });
      });
    }), (o, a) => null;
  }
});
export {
  pe as default
};