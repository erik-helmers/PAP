(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(company-idle-delay 0)
 '(custom-enabled-themes (quote (tango-dark)))
 '(inhibit-startup-screen t)
 '(transient-mark-mode t))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )

;; =========================== Automatic packages ============================

;; Packages: list the repositories containing them
(setq package-archives '(("melpa" . "http://melpa.milkbox.net/packages/")))

;; activate all the packages (in particular autoloads)
(require 'package)
(package-initialize)


;; ============================= Generic options =============================

;; Ajout au path de chargement
(setq-default load-path
  (cons (expand-file-name "~/.emacs.d/site-lisp") load-path))
(setq-default load-path
  (cons (expand-file-name "~/.emacs.d/elpa") load-path))

;; Supprimer le message d'ouverture
(setq inhibit-startup-message t inhibit-startup-echo-area-message t)

;; Afficher la ligne, la colonne, la date
(line-number-mode t)
(column-number-mode t)
(display-time-mode t)
(setq display-time-24hr-format t)

;; Display path file in frame title
(setq-default frame-title-format "%b (%f)")

;; Affiche la barre des menus mais pas la barre d'outil
(menu-bar-mode t)
(tool-bar-mode -1)

;; Transforme le bip sonore en bip lumineux
;(setq visible-bell t)

;; Afficher la barre de défilement à droite
(scroll-bar-mode t)
(set-scroll-bar-mode 'right)

;; Surligne lors d'un rechercher/remplacer
(setq search-highlight t query-replace-highlight t)

;; Si je cherche 2 espaces, je veux vraiment 2 espaces, et pas au moins 1
(setq search-whitespace-regexp -1)

;; Mise en surbriallance de la zone selectionnée
(transient-mark-mode t)

;; Supprime le texte selectionné lors de la saisie d'un nouveau texte
(delete-selection-mode t)

;; Remplace toutes les questions yes-no en y-n
(fset 'yes-or-no-p 'y-or-n-p)

;; Déplacement du curseur, de la souris, de la molette...
(require 'mwheel)
(mouse-wheel-mode t)
(setq scroll-preserve-screen-position t)
(setq track-eol -1)
(setq scroll-step 1)
(setq next-screen-context-lines 1)
(setq scroll-margin 1
  scroll-conservatively 100000
  scroll-up-aggressively 0.01
  scroll-down-aggressively 0.01)

;; Un « copier-coller » à la souris, insérer le texte au niveau du curseur
;(setq mouse-yank-at-point -1)

;; Configuration pour les fichiers backup
(setq make-backup-files nil)

;; Supprimer les backup en trop grand nombre
;(setq delete-old-versions t)

;; Ne pas sauvegarder les abréviations
(setq save-abbrevs nil)

;; Case insensitive completing file name
(setq read-file-name-completion-ignore-case t)


;; ============================ Raccourcis perso ============================

(defvar my-keys-minor-mode-map
  (let ((map (make-sparse-keymap)))
    (define-key map (kbd "M-<left>") 'windmove-left)
    (define-key map (kbd "M-<right>") 'windmove-right)
    (define-key map (kbd "M-<up>") 'windmove-up)
    (define-key map (kbd "M-<down>") 'windmove-down)
    map)
  "my-keys-minor-mode keymap.")

(define-minor-mode my-keys-minor-mode
  "A minor mode so that my key settings override annoying major modes."
  :init-value t
  :lighter " my-keys")

(my-keys-minor-mode t)

;; Auto-kill compilation process and recompile
(defun interrupt-and-recompile ()
  "Interrupt old compilation, if any, and recompile."
  (interactive)
  (ignore-errors
    (process-kill-without-query
     (get-buffer-process
      (get-buffer "*compilation*"))))
  (ignore-errors
    (kill-buffer "*compilation*"))
  (recompile))

;; auto-scroll in the compilation buffer
(setq compilation-scroll-output 'first-error)

(global-set-key [f1] 'comment-dwim)
(global-set-key [f2] 'undo)
(global-set-key [f3] 'grep)
(global-set-key [f4] 'goto-line)
(global-set-key [f5] 'compile)
(global-set-key [f6] 'interrupt-and-recompile)
(global-set-key [f7] 'next-error)
(global-set-key [f8] 'caml-types-show-type)

;; Automatically resize widow when splitting
(global-set-key
 (kbd "C-x 2") (lambda () (interactive) (split-window-below) (balance-windows)))
(global-set-key
 (kbd "C-x 3") (lambda () (interactive) (split-window-right) (balance-windows)))
(global-set-key
 (kbd "C-x 0") (lambda () (interactive) (delete-window) (balance-windows)))

;; Autocomplete
(add-hook 'after-init-hook 'global-company-mode)
(autoload 'company-mode "company" nil t)
(require 'company)
(global-set-key (kbd "C-/") 'company-complete)
(setq company-dabbrev-downcase nil)


;; ====================== Divers pour la programmation ======================

;; Whitespace
(require 'whitespace)
(setq whitespace-style '(face trailing empty lines-tail tabs tab-mark))
(setq whitespace-space 'whitespace-hspace)
(setq whitespace-line-column 80)
;(add-hook 'prog-mode-hook 'whitespace-mode)
(global-whitespace-mode 1)
(custom-set-faces
  '(whitespace-space ((t (:bold t :foreground "gray75"))))
  '(whitespace-empty ((t (:foreground "firebrick" :background "SlateGray1"))))
  '(whitespace-hspace ((t (:foreground "white" :background "red"))))
  '(whitespace-indentation ((t (:foreground "firebrick" :background "beige"))))
  '(whitespace-line ((t (:foreground "black" :background "red"))))
  '(whitespace-newline ((t (:foreground "orange" :background "blue"))))
  '(whitespace-space-after-tab ((t (:foreground "black" :background "green"))))
  '(whitespace-space-before-tab ((t (:foreground "black" :background "DarkOrange"))))
  '(whitespace-tab ((t (:foreground "red" :background "yellow"))))
  '(whitespace-trailing ((t (:foreground "red" :background "yellow")))))

;; Suppression des espaces à la sauvegarde
;(add-hook 'before-save-hook 'delete-trailing-whitespace)

;; Terminer les fichiers par une nouvelle ligne
(setq require-final-newline t)

;; Remplacer les tabulations par des espaces
(setq-default indent-tabs-mode nil)

;; Montrer la correspondance des parenthèses
(require 'paren)
(show-paren-mode t)
(setq blink-matching-paren t)
(setq blink-matching-paren-on-screen t)
(setq show-paren-style 'expression)
(setq blink-matching-paren-dont-ignore-comments t)


;; =================================== BASH ==================================

(setq-default sh-basic-offset 2)
(setq-default sh-indentation 2)


;; ================================== OCAML ==================================

(add-to-list 'load-path (concat
   (replace-regexp-in-string "\n$" ""
      (shell-command-to-string "opam config var share"))
   "/emacs/site-lisp"))

(require 'caml-font)

;; Load merlin-mode
(require 'merlin)
;; Start merlin on ocaml files
(add-hook 'tuareg-mode-hook 'merlin-mode)
;; Use opam switch to lookup ocamlmerlin binary.
(setq merlin-command 'opam)
(add-hook 'caml-mode-hook 'merlin-mode)
;; Enable auto-complete
;(setq merlin-use-auto-complete-mode 'easy)
;(setq merlin-use-auto-complete-mode t)
;(add-hook 'caml-mode-hook 'merlin-mode)
;; Make company aware of merlin
(add-to-list 'company-backends 'merlin-company-backend)
;; Enable company on merlin managed buffers
(add-hook 'merlin-mode-hook 'company-mode)


(require 'ocp-indent)

(setq auto-mode-alist (cons '("\\.ml[iylp]?$" . caml-mode) auto-mode-alist))
(autoload 'caml-mode "caml" "Major mode for editing Caml code." t)
(autoload 'camldebug "camldebug" (interactive) "Debug caml mode")
(autoload 'run-caml "inf-caml" "Run an inferior Caml process." t)


;; ================================== C/C++ ==================================

(setq-default c-default-style "linux")
(setq-default c-basic-offset 4)
