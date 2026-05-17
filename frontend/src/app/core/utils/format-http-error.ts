import { HttpErrorResponse } from '@angular/common/http';

/** Corps d'erreur API (DRF, etc.) depuis HttpErrorResponse ou objet quelconque. */
export function getHttpErrorPayload(err: unknown): unknown {
  if (err instanceof HttpErrorResponse) {
    return err.error;
  }
  if (err && typeof err === 'object' && 'error' in err) {
    return (err as { error: unknown }).error;
  }
  return undefined;
}

/** Indique si le backend a signalé une erreur sur un champ d’inscription. */
export function registerFieldHasError(err: unknown, field: string): boolean {
  const body = getHttpErrorPayload(err);
  if (body == null || typeof body !== 'object' || Array.isArray(body)) {
    return false;
  }
  const v = (body as Record<string, unknown>)[field];
  if (v == null) return false;
  if (Array.isArray(v)) return v.length > 0;
  if (typeof v === 'string') return v.length > 0;
  return true;
}

/** Normalize DRF / Django REST field values to user-visible strings. */
function messagesFromFieldValue(val: unknown): string[] {
  if (val == null) return [];
  if (typeof val === 'string') return [val];
  if (Array.isArray(val)) return val.flatMap(messagesFromFieldValue);
  if (typeof val === 'object') {
    const o = val as Record<string, unknown>;
    if (typeof o['string'] === 'string') return [o['string'] as string];
    if (typeof o['detail'] === 'string') return [o['detail'] as string];
    if (typeof o['message'] === 'string') return [o['message'] as string];
  }
  return [];
}

function looksLikeUniqueOrDuplicate(messages: string[]): boolean {
  const t = messages.join(' ').toLowerCase();
  return (
    t.includes('already exists') ||
    t.includes('already been taken') ||
    t.includes('déjà') ||
    t.includes('unique') ||
    t.includes('exists') ||
    t.includes('utilisateur with this') // message Django/DRF bancal (EN+FR)
  );
}

function friendlyDuplicateAccount(keys: string[], messages: string[]): string {
  const email = keys.includes('email');
  const username = keys.includes('username');
  if ((email || username) && looksLikeUniqueOrDuplicate(messages)) {
    return "Cette adresse e-mail ou ce nom d'utilisateur est déjà utilisé. Connectez-vous ou modifiez l'e-mail.";
  }
  if (email && looksLikeUniqueOrDuplicate(messages)) {
    return "Cette adresse e-mail est déjà utilisée. Connectez-vous ou utilisez une autre adresse.";
  }
  if (username && looksLikeUniqueOrDuplicate(messages)) {
    return "Ce nom d'utilisateur est déjà pris. Choisissez-en un autre ou connectez-vous.";
  }
  return '';
}

function formatErrorBody(body: unknown): { text: string; fieldKeys: string[] } {
  if (body == null || body === '') {
    return { text: '', fieldKeys: [] };
  }

  if (typeof body === 'string') {
    try {
      const parsed = JSON.parse(body) as unknown;
      return formatErrorBody(parsed);
    } catch {
      return { text: body.trim(), fieldKeys: [] };
    }
  }

  if (typeof body !== 'object' || Array.isArray(body)) {
    return { text: String(body), fieldKeys: [] };
  }

  const o = body as Record<string, unknown>;

  if (typeof o['error'] === 'string') {
    return { text: o['error'] as string, fieldKeys: [] };
  }

  // Format renvoyé par core.exceptions.custom_exception_handler
  if (typeof o['message'] === 'string' && o['message'].trim()) {
    return { text: o['message'].trim(), fieldKeys: [] };
  }

  if (o['detail'] != null) {
    const parts = messagesFromFieldValue(o['detail']);
    if (parts.length) return { text: [...new Set(parts)].join(' '), fieldKeys: [] };
  }

  const skipKeys = new Set(['detail', 'status', 'status_code', 'errors']);
  const parts: string[] = [];
  const fieldKeys: string[] = [];
  for (const key of Object.keys(o)) {
    if (skipKeys.has(key)) continue;
    fieldKeys.push(key);
    parts.push(...messagesFromFieldValue(o[key]));
  }
  const unique = [...new Set(parts.filter(Boolean))];
  let text = unique.join(' ');

  const friendly = friendlyDuplicateAccount(fieldKeys, unique);
  if (friendly) {
    text = friendly;
  }

  return { text, fieldKeys };
}

/**
 * Build a single line or short message from an HttpErrorResponse-like object
 * (handles DRF 400 bodies, `{ error: string }`, `{ detail: ... }`, string bodies).
 */
export function formatHttpErrorMessage(err: unknown): string {
  const e = err as { message?: string; status?: number };
  const body = getHttpErrorPayload(err);

  if (body == null || body === '') {
    if (err instanceof HttpErrorResponse && err.status === 400) {
      return 'Données invalides. Vérifiez les champs du formulaire.';
    }
    if (typeof e?.message === 'string' && e.message.includes('0 Unknown Error')) {
      return 'Impossible de contacter le serveur.';
    }
    return '';
  }

  let { text } = formatErrorBody(body);
  if (/invalid token/i.test(text)) {
    text = 'Session expirée ou jeton invalide. Réessayez de vous connecter.';
  }
  return text;
}
