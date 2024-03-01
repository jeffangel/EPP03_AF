import { Injectable, Injector } from '@angular/core';
import { HttpInterceptor } from '@angular/common/http';

import { AuthService } from '../services/auth.service';

@Injectable()
export class CasesInterceptorInterceptor implements HttpInterceptor {
  
  constructor(private injector: Injector) {}

  intercept(req:any, next:any) {
    let authService = this.injector.get(AuthService)
    let tokenizedReq = req.clone(
      {
/*         headers: req.headers.set('Email', authService.getToken()) */
      }
    )
    return next.handle(tokenizedReq)
  }
}