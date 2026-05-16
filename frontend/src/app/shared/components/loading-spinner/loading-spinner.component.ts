import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

/**
 * Composant de spinner/loader réutilisable
 */
@Component({
  selector: 'app-loading-spinner',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="flex justify-center items-center py-12">
      <div class="text-center">
        <div
          class="h-12 w-12 border-4 rounded-full animate-spin mb-4 mx-auto"
          [ngClass]="'border-' + (color || 'blue') + '-200 border-t-' + (color || 'blue') + '-700'"
        ></div>
        <p class="text-slate-600">{{ message || 'Chargement...' }}</p>
      </div>
    </div>
  `,
  styles: [],
})
export class LoadingSpinnerComponent {
  @Input() message: string = 'Chargement...';
  @Input() color: string = 'blue'; // blue, orange, green, etc.
}
