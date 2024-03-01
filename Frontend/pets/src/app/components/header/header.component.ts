import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { Subscription } from 'rxjs';

import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent {

  is_logged$:boolean = false
  subscription: Subscription

  constructor(private authService: AuthService,
              private router: Router) {
                this.subscription = this.authService.logged_in.subscribe((data) => {
                  this.is_logged$ = data
                })
               }

  logout() {
    this.authService.logout_user().subscribe({
      next: () => {
          localStorage.removeItem('session')
          this.router.navigate(['/login'])
      },
      error: error => {
        console.error('Ocurrió un error: ', error)
        this.router.navigate(['/maintenance'])
      }      
    })
  }

}
