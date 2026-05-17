import { Component, Input, Output, EventEmitter } from '@angular/core';

/**
 * Composant d'erreur réutilisable
 */
@Component({
  selector: 'app-error-message',
  standalone: true,
  imports: [],
  template: `
    <div class="rounded-2xl bg-red-50 p-6 border-l-4 border-red-500">
      <h3 class="font-semibold text-red-900">⚠️ {{ title || 'Erreur' }}</h3>
      <p class="mt-2 text-red-800">{{ message }}</p>
      @if (showRetryButton) {
        <button
          type="button"
          (click)="emitRetry()"
          class="mt-4 inline-block px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
        >
          Réessayer
        </button>
      }
    </div>
  `,
  styles: [],
})
export class ErrorMessageComponent {
  @Input() title: string = 'Erreur';
  @Input() message: string = '';
  /** Afficher le bouton « Réessayer » (désactiver avec [showRetryButton]="false") */
  @Input() showRetryButton = true;
  @Output() retry = new EventEmitter<void>();

  emitRetry(): void {
    this.retry.emit();
  }
}
