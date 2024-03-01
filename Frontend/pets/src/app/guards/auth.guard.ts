import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, RouterStateSnapshot, UrlTree, Router } from '@angular/router';
import { Observable, map } from 'rxjs';

import { AuthService } from '../services/auth.service'
import { bootstrapApplication } from '@angular/platform-browser';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  validation: boolean = false;

  constructor(private authService: AuthService,
              private router: Router) { }
  
  canActivate(
    route: ActivatedRouteSnapshot, state: RouterStateSnapshot): 
    Observable<boolean> | boolean {  
    return this.check_session(state.url)
  }
  check_session(state_url:String) {
    return this.authService.session_user().pipe(
      map(data => {
        console.log(data['msg'])
         if (data['msg'] != 'invalid_token') {
          localStorage.setItem('user_email', data['msg'])
          return true
         }
         else {
           this.router.navigate(['/login'], {queryParams: {redirectUrl: state_url}})
           return false
         }    
      })
    )
  }
  
}
