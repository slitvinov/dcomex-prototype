rng(123456);
Nd = 40;
alpha =  2;
beta  = -2;
sigma =  2;
data.x = linspace(1, 10, Nd);
data.y = alpha * data.x + beta + normrnd(0,sigma,1,Nd);
data.Nd = Nd;
max_cLen = 1;
Ns = 100;
beta2 = 0.04;
sys_para.eps = 0.04;
sys_para.N_dim = 3;
sys_para.hard_bds = [ -5 -5  0;
		      5  5 10];
sys_para.conf = 0.68;
sys_para.extend_bds = [1 1 1];
sys_para.opt_iniP = 1e-8;
x = zeros(Ns,sys_para.N_dim);
ln_f = zeros(Ns, 1);
for j = 1:sys_para.N_dim
  sys_para.pri.para{j} = sys_para.hard_bds(:, j);
  x(:, j) = random('Uniform', sys_para.pri.para{j}(1),sys_para.pri.para{j}(2), Ns,1);
  ln_f = ln_f + log(pdf('Uniform',x(:,j), sys_para.pri.para{j}(1), sys_para.pri.para{j}(2)));
end
for i = 1:Ns
  out(i).x = x(i,:);
  out(i).Ns = 1;
  [out(i).f,out(i).out_f] = loglike(x(i,:),data);
  out(i).pri = ln_f(i);
end
gen = 1;
info.Ns = zeros(Ns,1);
info.sigma = zeros(sys_para.N_dim);
pri = zeros(Ns,1);
f = zeros(Ns,1);
p = 0;
End = false;
while 1
  for i = 1:Ns
    x(i,:) = out(i).x;
    info.Ns(i) = out(i).Ns;
    pri(i) = out(i).pri;
    f(i) = out(i).f;
    info.out_f(i) = out(i).out_f;
  end
  if End; break; end
  tmp = find(info.Ns > 1);
  for i = 1:length(tmp)
    f(end+1:end+info.Ns(tmp(i))-1) = f(tmp(i));
  end
  old_p = p;
  plo = p;
  phi = 2;
  while phi - plo > 1e-6
    p = (plo + phi) / 2;
    temp = (p - old_p) * f;
    M1 = logsumexp(temp) - log(Ns);
    M2 = logsumexp(2 * temp) - log(Ns);
    if M2 - 2 * M1 > log(2); phi = p; else plo = p; end
  end
  if p > 1
    p = 1;
    End = true;
  end
  dp = p - old_p;
  weight = softmax(dp*f);
  x0 = x - weight' * x;
  for i=1:sys_para.N_dim
    for j=i:sys_para.N_dim
      info.sigma(i, j) = beta2 * weight' * (x0(:, i) .* x0(:, j));
      info.sigma(j, i) = info.sigma(i, j);
    end
  end
  cum_weight = [0 cumsum(weight)'];
  ind = arrayfun(@(x) find(cum_weight <= x, 1, 'last'), rand(1, Ns));
  x = x(ind,:);
  f = f(ind,:);
  pri = pri(ind,:);
  out_f = info.out_f(ind);
  for i = 1:Ns
    xo = x(i,:);
    gradiento = p*out_f(i).gradient(:);
    if out_f(i).check ~= 0
      SIG = info.sigma;
      do_correction = 1;
    else
      posdef = out_f(i).posdef;
      V = out_f(i).eig.V;
      D = out_f(i).eig.D;
      Dp = D/p;
      do_correction = do_eigendirection_check( x(i, :), Dp, V, sys_para);
      do_correction = do_correction || ~posdef;
      if do_correction
	Dp_new = Dp;
	if ~posdef
	  E = sort(eig(info.sigma));
	  Dp_new(Dp_new<=0) = E(1:sum(Dp_new<=0));
	  Dp_new(Dp_new<0) = 0;
	end
	if do_eigendirection_check( x(i, :), Dp_new, V, sys_para)
	  Dp_new  = adapt_evals_to_bounds(x(i, :), Dp_new, V, sys_para);
	end
	SIG =  V * diag(Dp_new) * V';
      else
	SIG = out_f(i).inv_G/old_p;
      end
    end
    SIG = (SIG + SIG.') / 2;
    [~,err_flg] = cholcov(SIG);
    if err_flg ~= 0
      SIG = info.sigma;
      warning('cov correction failed, setting SIGMA = info.sigma');
    end
    lnfo_f = f(i);
    lnfo_pri = pri(i);
    o_check = out_f(i).check;
    out(i).Ns = 0;
    out(i).x = xo;
    out(i).f = lnfo_f;
    out(i).out_f = out_f(i);
    bds = sys_para.hard_bds;
    if o_check == 0 || o_check == 2
      xc = mvnrnd( xo(:) + 0.5*sys_para.eps*SIG*gradiento, sys_para.eps*SIG );
    elseif o_check == 1
      xc = mvnrnd( xo(:), sys_para.eps*SIG );
    else
      error('invalid state: o_check');
    end
    if any(xc < bds(1,:)) || any(xc > bds(2,:))
      out(i).Ns(end) = out(i).Ns(end) + 1;
    else
      [lnfc_f,outc_f] = loglike(xc,data);
      lnfc_pri = 0;
      for j = 1:sys_para.N_dim
	lnfc_pri = lnfc_pri + log(pdf('Uniform',xc(:,j), sys_para.pri.para{j}(1), sys_para.pri.para{j}(2)));
      end
      c_check = outc_f.check;
      gradientc = p * outc_f.gradient(:);
      if o_check == 0 || o_check == 2
	if c_check == 0 || c_check == 2
	  tmpc = xc(:) - xo(:) - 0.5*sys_para.eps*SIG*gradiento(:);
	  tmpo = xo(:) - xc(:) - 0.5*sys_para.eps*SIG*gradientc(:);
	  qc = -(tmpc'*(sys_para.eps*SIG\tmpc))/2;
	  qo = -(tmpo'*(sys_para.eps*SIG\tmpo))/2;
	  r = exp(old_p*...
		  (lnfc_f - lnfo_f) + (lnfc_pri - lnfo_pri) + ...
		  qo - qc);
	elseif c_check == 1
	  r = 0.0;
	else
	  error('invalid state: c_check');
	end
      elseif o_check == 1
	r = exp(p * (lnfc_f - lnfo_f) + (lnfc_pri - lnfo_pri));
      else
	error('invalid state: o_check');
      end
      r = min(1,r);
      if find(mnrnd(1,[r,1-r])) == 1
	out(i).x(end+1,:) = xc;
	out(i).Ns(end+1) = 1;
	out(i).f(end+1) = lnfc_f;
	out(i).pri(end+1) = lnfc_pri;
	out(i).out_f(end+1) = outc_f;
      else
	out(i).Ns(end) = out(i).Ns(end) + 1;
      end
    end
    if out(i).Ns(1) == 0
      out(i).x(1,:) = [];
      out(i).Ns(1) = [];
      out(i).f(1) = [];
      out(i).pri(1) = [];
      out(i).out_f(1) = [];
    end
  end
  gen = gen + 1;
end
disp(mean(x));
function do_correction = do_eigendirection_check( x, Dp, V, local_para)
  x = x(:);
  df = length(x);
  chi = chi2inv(local_para.conf,df);
  do_correction = 0;
  for l = 1:local_para.N_dim
    sc = sqrt(Dp(l)/chi);
    pp = x + sc*V(:,l);
    if ~in_the_box(pp,local_para.hard_bds)
      do_correction = 1;
      break;
    end
    pm = x - sc*V(:,l);
    if ~in_the_box(pm,local_para.hard_bds)
      do_correction = 1;
      break;
    end
  end
end
function [Dp] = adapt_evals_to_bounds( x, Dp, V, local_para)
  x = x(:);
  df = length(x);
  chi2 = chi2inv(local_para.conf,df);
  bds = local_para.hard_bds;
  width = bds(2,:)-bds(1,:);
  bds(2,:) = bds(2,:)+width.*local_para.extend_bds;
  bds(1,:) = bds(1,:)-width.*local_para.extend_bds;
  for l = 1:local_para.N_dim
    sc = sqrt(Dp(l)*chi2);
    pp = x + sc*V(:,l);
    flag = pp' <= bds(1,:);
    if any(flag > 0)
      c = abs(1./V(flag,l) .* (bds(1,flag)'-x(flag)));
      sc = min(c(:));
    end
    pp = x + sc*V(:,l);
    flag = pp' >= bds(2,:);
    if any(flag > 0)
      c = abs(1./V(flag,l) .* (bds(2,flag)'-x(flag)));
      sc = min(c(:));
    end
    pm = x - sc*V(:,l);
    flag = pm' <= bds(1,:);
    if any(flag > 0)
      c = abs(1./V(flag,l) .* (bds(1,flag)'-x(flag)));
      sc = min(c(:));
    end
    pm = x - sc*V(:,l);
    flag = pm' >= bds(2,:);
    if any(flag > 0)
      c = abs(1./V(flag,l) .* (bds(2,flag)'-x(flag)));
      sc = min(c(:));
    end
    Dp(l) = sc^2/chi2;
  end
end
function flag = in_the_box( x, Box )
  x = x(:)';
  flag = ~any( x<Box(1,:) | x>Box(2,:) );
end
